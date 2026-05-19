(function () {
  "use strict";

  const ACTION_COPY = {
    accept_extraction: "accept extraction",
    ask_for_clarification: "ask for clarification",
    retrieve_more_context: "retrieve more context",
    flag_for_review: "flag for review",
    defer: "defer",
  };

  const ACTION_SHORT_COPY = {
    accept_extraction: "accept",
    ask_for_clarification: "clarify",
    retrieve_more_context: "retrieve",
    flag_for_review: "review",
    defer: "defer",
  };

  const STATE_COPY = {
    stable: {
      action: "accept_extraction",
      title: "Stable",
      explanation:
        "The same next action keeps winning with a wide margin. In a document queue, this is the boring-good case: the workflow can usually continue if the task is in scope.",
    },
    binary_ambiguity: {
      action: "ask_for_clarification",
      title: "Binary ambiguity",
      explanation:
        "The cloud is stretched mostly between two plausible choices. This is the contract-date situation: both interpretations can be real, so a targeted question is more useful than a generic review flag.",
    },
    diffuse_uncertainty: {
      action: "retrieve_more_context",
      title: "Diffuse uncertainty",
      explanation:
        "Support is spread across several actions. That often reads like missing evidence, incomplete context, or a document packet that does not yet contain the source needed to act.",
    },
    boundary_sensitive: {
      action: "flag_for_review",
      title: "Boundary sensitive",
      explanation:
        "The samples move coherently near a low-margin boundary. The value may be legible, but a small rule, threshold, or context shift changes the action.",
    },
    regime_shift: {
      action: "defer",
      title: "Regime shift",
      explanation:
        "Early and late observations disagree. In a multi-page packet, that is the moment to pause and re-read the trajectory rather than treating the case as one static extraction.",
    },
  };

  const FIXTURE_STATE_COPY = {
    stable: "stable",
    binary_ambiguous: "ambiguous",
    diffuse: "diffuse",
    boundary_sensitive: "sensitive",
    drifting: "drifting",
  };

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function format(value, digits = 3) {
    return Number.isFinite(value) ? value.toFixed(digits) : "0.000";
  }

  function humanizeAction(label) {
    return ACTION_COPY[label] || label.replaceAll("_", " ");
  }

  function shortenAction(label) {
    return ACTION_SHORT_COPY[label] || humanizeAction(label);
  }

  function dot(a, b) {
    return a.reduce((sum, value, index) => sum + value * b[index], 0);
  }

  function norm(values) {
    return Math.sqrt(dot(values, values));
  }

  function normalizeVector(values) {
    const length = norm(values);
    if (length <= 1e-15) {
      return values.map(() => 0);
    }
    return values.map((value) => value / length);
  }

  function normalizeProbabilities(rows) {
    return rows.map((row) => {
      const cleaned = row.map((value) => Math.max(1e-12, Number(value) || 0));
      const total = cleaned.reduce((sum, value) => sum + value, 0);
      return cleaned.map((value) => value / total);
    });
  }

  function generateVariationRows(rows, state, counter) {
    const amplitudeByState = {
      stable: 0.012,
      binary_ambiguous: 0.035,
      diffuse: 0.045,
      boundary_sensitive: 0.03,
      drifting: 0.04,
    };
    const amplitude = amplitudeByState[state] || 0.025;
    const varied = rows.map((row, rowIndex) =>
      row.map((value, columnIndex) => {
        const wave = Math.sin((counter + 1) * (rowIndex + 2) * (columnIndex + 3));
        const offset = amplitude * wave;
        return Math.max(0.01, value + offset);
      })
    );
    return normalizeProbabilities(varied);
  }

  function sqrtEmbed(rows) {
    return rows.map((row) => normalizeVector(row.map((value) => Math.sqrt(value))));
  }

  function sphereExp(mean, tangent) {
    const theta = norm(tangent);
    if (theta <= 1e-12) {
      return mean.slice();
    }
    const cosTheta = Math.cos(theta);
    const sinTheta = Math.sin(theta);
    return normalizeVector(mean.map((value, index) => cosTheta * value + (sinTheta / theta) * tangent[index]));
  }

  function sphereLog(mean, point) {
    const cosine = clamp(dot(mean, point), -1, 1);
    const theta = Math.acos(cosine);
    if (theta <= 1e-12) {
      return mean.map(() => 0);
    }
    const sine = Math.sin(theta);
    const scale = theta / Math.max(sine, 1e-12);
    return point.map((value, index) => scale * (value - cosine * mean[index]));
  }

  function intrinsicMeanSphere(points, maxIter = 32) {
    let mean = normalizeVector(
      points[0].map((_, column) => points.reduce((sum, point) => sum + point[column], 0))
    );
    for (let iter = 0; iter < maxIter; iter += 1) {
      const averageTangent = mean.map(() => 0);
      points.forEach((point) => {
        const tangent = sphereLog(mean, point);
        tangent.forEach((value, index) => {
          averageTangent[index] += value / points.length;
        });
      });
      if (norm(averageTangent) < 1e-10) {
        break;
      }
      mean = sphereExp(mean, averageTangent);
    }
    return mean;
  }

  function covarianceTensor(tangents) {
    const dimension = tangents[0].length;
    const tensor = Array.from({ length: dimension }, () => Array(dimension).fill(0));
    tangents.forEach((tangent) => {
      for (let row = 0; row < dimension; row += 1) {
        for (let column = 0; column < dimension; column += 1) {
          tensor[row][column] += (tangent[row] * tangent[column]) / tangents.length;
        }
      }
    });
    return tensor;
  }

  function jacobiEigenvalues(matrix) {
    const n = matrix.length;
    const a = matrix.map((row) => row.slice());
    for (let iter = 0; iter < 80; iter += 1) {
      let p = 0;
      let q = 1;
      let maxValue = Math.abs(a[p][q]);
      for (let i = 0; i < n; i += 1) {
        for (let j = i + 1; j < n; j += 1) {
          const candidate = Math.abs(a[i][j]);
          if (candidate > maxValue) {
            maxValue = candidate;
            p = i;
            q = j;
          }
        }
      }
      if (maxValue < 1e-12) {
        break;
      }
      const app = a[p][p];
      const aqq = a[q][q];
      const apq = a[p][q];
      const phi = 0.5 * Math.atan2(2 * apq, aqq - app);
      const c = Math.cos(phi);
      const s = Math.sin(phi);
      for (let k = 0; k < n; k += 1) {
        const aik = a[p][k];
        const aqk = a[q][k];
        a[p][k] = c * aik - s * aqk;
        a[q][k] = s * aik + c * aqk;
      }
      for (let k = 0; k < n; k += 1) {
        const akp = a[k][p];
        const akq = a[k][q];
        a[k][p] = c * akp - s * akq;
        a[k][q] = s * akp + c * akq;
      }
      a[p][q] = 0;
      a[q][p] = 0;
    }
    return a.map((row, index) => Math.max(0, row[index])).sort((left, right) => right - left);
  }

  function meanProbability(rows) {
    return rows[0].map((_, column) => rows.reduce((sum, row) => sum + row[column], 0) / rows.length);
  }

  function topIndices(values) {
    return values.map((value, index) => ({ value, index })).sort((left, right) => right.value - left.value);
  }

  function topSequence(rows, labels) {
    return rows.map((row) => labels[topIndices(row)[0].index]);
  }

  function switchRate(sequence) {
    if (sequence.length <= 1) {
      return 0;
    }
    let switches = 0;
    for (let index = 1; index < sequence.length; index += 1) {
      if (sequence[index] !== sequence[index - 1]) {
        switches += 1;
      }
    }
    return switches / (sequence.length - 1);
  }

  function halfGeodesicDistance(rows) {
    if (rows.length < 4) {
      return 0;
    }
    const midpoint = Math.floor(rows.length / 2);
    const first = sqrtEmbed([meanProbability(rows.slice(0, midpoint))])[0];
    const second = sqrtEmbed([meanProbability(rows.slice(midpoint))])[0];
    return Math.acos(clamp(dot(first, second), -1, 1));
  }

  function diagnoseProbabilityCloud(rows, labels) {
    const probs = normalizeProbabilities(rows);
    const points = sqrtEmbed(probs);
    const mean = intrinsicMeanSphere(points);
    const tangents = points.map((point) => sphereLog(mean, point));
    const tensor = covarianceTensor(tangents);
    const eigenvalues = jacobiEigenvalues(tensor);
    const totalDispersion = eigenvalues.reduce((sum, value) => sum + value, 0);
    const pc1Fraction = totalDispersion > 1e-12 ? eigenvalues[0] / totalDispersion : 0;
    const anisotropyRatio = eigenvalues[1] > 1e-12 ? eigenvalues[0] / eigenvalues[1] : eigenvalues[0] > 0 ? Infinity : 0;
    const meanProb = meanProbability(probs);
    const sortedMean = topIndices(meanProb);
    const meanMargin = sortedMean[0].value - sortedMean[1].value;
    const sequence = topSequence(probs, labels);
    const topLabelSwitchRate = switchRate(sequence);
    const halfDistance = halfGeodesicDistance(probs);

    let state = "diffuse_uncertainty";
    if (halfDistance > 0.45 && topLabelSwitchRate > 0) {
      state = "regime_shift";
    } else if (meanMargin > 0.35 && totalDispersion < 0.015) {
      state = "stable";
    } else if (halfDistance > 0.12 && pc1Fraction > 0.8 && meanMargin < 0.2) {
      state = "boundary_sensitive";
    } else if (pc1Fraction > 0.8 && meanMargin < 0.15) {
      state = "binary_ambiguity";
    }

    return {
      state,
      workflowAction: STATE_COPY[state].action,
      meanProbability: meanProb,
      topLabels: sortedMean.slice(0, 3).map((item) => labels[item.index]),
      topSequence: sequence,
      metrics: {
        total_dispersion: totalDispersion,
        pc1_fraction: pc1Fraction,
        anisotropy_ratio: anisotropyRatio,
        mean_margin: meanMargin,
        half_geodesic_distance: halfDistance,
        top_label_switch_rate: topLabelSwitchRate,
      },
    };
  }

  function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) {
      element.className = className;
    }
    if (text !== undefined) {
      element.textContent = text;
    }
    return element;
  }

  function renderProbabilityBars(container, labels, values) {
    const bars = createElement("div", "probability-bars");
    labels.forEach((label, index) => {
      const row = createElement("div", "probability-bar-row");
      row.append(createElement("span", "probability-bar-label", humanizeAction(label)));
      const track = createElement("span", "probability-bar-track");
      const fill = createElement("span", "probability-bar-fill");
      fill.style.width = `${clamp(values[index], 0, 1) * 100}%`;
      track.append(fill);
      row.append(track);
      row.append(createElement("span", "probability-bar-value", format(values[index], 2)));
      bars.append(row);
    });
    container.append(bars);
  }

  function renderPayload(container, scenario, labels, rows) {
    container.textContent = JSON.stringify(
      {
        source: "probability_cloud",
        label: scenario.id,
        labels,
        probabilities: normalizeProbabilities(rows).map((row) => row.map((value) => Number(value.toFixed(6)))),
      },
      null,
      2
    );
  }

  function readRows(root) {
    const rowElements = Array.from(root.querySelectorAll("[data-row-index]"));
    return rowElements.map((rowElement) =>
      Array.from(rowElement.querySelectorAll("input")).map((input) => Number(input.value))
    );
  }

  function updateRowSums(root) {
    root.querySelectorAll("[data-row-index]").forEach((rowElement) => {
      const sum = Array.from(rowElement.querySelectorAll("input")).reduce((total, input) => total + Number(input.value || 0), 0);
      const sumCell = rowElement.querySelector("[data-row-sum]");
      sumCell.textContent = format(sum, 2);
      sumCell.classList.toggle("is-off", Math.abs(sum - 1) > 0.02);
    });
  }

  function renderMatrixEditor(container, labels, rows) {
    const table = createElement("table", "live-demo-table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    ["pass", ...labels.map(humanizeAction), "sum"].forEach((label) => {
      headRow.append(createElement("th", null, label));
    });
    thead.append(headRow);
    table.append(thead);

    const tbody = document.createElement("tbody");
    rows.forEach((row, rowIndex) => {
      const tr = document.createElement("tr");
      tr.dataset.rowIndex = String(rowIndex);
      tr.append(createElement("td", null, String(rowIndex + 1)));
      row.forEach((value, columnIndex) => {
        const td = document.createElement("td");
        const input = document.createElement("input");
        input.type = "number";
        input.min = "0";
        input.max = "1";
        input.step = "0.001";
        input.value = value.toFixed(3);
        input.dataset.columnIndex = String(columnIndex);
        td.append(input);
        tr.append(td);
      });
      const sumCell = createElement("td", "row-sum");
      sumCell.dataset.rowSum = "true";
      tr.append(sumCell);
      tbody.append(tr);
    });
    table.append(tbody);

    container.replaceChildren(table);
    updateRowSums(container);
  }

  function renderContext(container, scenario) {
    container.innerHTML = "";
    const context = document.createElement("p");
    context.append(createElement("strong", null, "Document situation: "), document.createTextNode(scenario.document_context));
    const value = document.createElement("p");
    value.append(createElement("strong", null, "Candidate extraction: "), document.createTextNode(scenario.candidate_value));
    const why = document.createElement("p");
    why.append(createElement("strong", null, "Why it feels real: "), document.createTextNode(scenario.why_it_feels_real));
    container.append(context, value, why);
  }

  function renderScenarioButtons(container, scenarios, activeScenario, onSelect) {
    container.innerHTML = "";
    const intro = createElement(
      "p",
      "microcopy",
      "One-click synthetic cases. These are the fastest way to see how the same diagnostic maps different document situations to different workflow actions."
    );
    const buttons = createElement("div", "live-demo-case-buttons");
    scenarios.forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "case-button";
      button.dataset.scenarioId = item.id;
      button.setAttribute("aria-pressed", String(item.id === activeScenario.id));
      button.append(
        createElement("span", null, item.name),
        createElement("small", null, `${FIXTURE_STATE_COPY[item.expected_state] || item.expected_state} -> ${shortenAction(item.expected_action)}`)
      );
      button.addEventListener("click", () => onSelect(item));
      buttons.append(button);
    });
    container.append(intro, buttons);
  }

  function renderOutput(container, labels, diagnostic) {
    const stateInfo = STATE_COPY[diagnostic.state];
    container.innerHTML = "";
    const title = createElement("h4", null, "Generated diagnostic readout");
    const stateLine = createElement("p");
    const pill = createElement("span", "state-pill", stateInfo.title);
    stateLine.append(pill);
    const action = createElement("p");
    action.innerHTML = `Workflow action: <code>${diagnostic.workflowAction}</code>`;
    const top = createElement("p", "microcopy", `Top labels: ${diagnostic.topLabels.map(humanizeAction).join(", ")}`);
    const note = createElement(
      "p",
      "microcopy",
      "This readout is a routing hint for the next workflow step, not a claim that the extracted value is correct."
    );

    const metrics = createElement("div", "live-metric-grid");
    [
      ["mean margin", diagnostic.metrics.mean_margin],
      ["PC1 fraction", diagnostic.metrics.pc1_fraction],
      ["dispersion", diagnostic.metrics.total_dispersion],
      ["half-cloud drift", diagnostic.metrics.half_geodesic_distance],
    ].forEach(([label, value]) => {
      const metric = createElement("div", "live-metric");
      metric.append(createElement("span", null, label), createElement("strong", null, format(value, 3)));
      metrics.append(metric);
    });

    const barTitle = createElement("p", "microcopy", "Mean next-action probabilities");
    const sequence = createElement("div", "sequence-row");
    diagnostic.topSequence.forEach((label, index) => {
      const chip = createElement("span", "sequence-chip", `${index + 1}: ${shortenAction(label)}`);
      chip.title = humanizeAction(label);
      sequence.append(chip);
    });

    container.append(title, stateLine, action, top, note, metrics, barTitle);
    renderProbabilityBars(container, labels, diagnostic.meanProbability);
    container.append(createElement("p", "microcopy", "Top action sequence"), sequence);
  }

  function renderExplanation(container, scenario, diagnostic) {
    const stateInfo = STATE_COPY[diagnostic.state];
    container.innerHTML = "";
    const paragraph = document.createElement("p");
    paragraph.innerHTML = `<strong>Human reading:</strong> ${stateInfo.explanation} For <strong>${scenario.name}</strong>, the live runner maps the probability cloud to <code>${diagnostic.workflowAction}</code>.`;
    container.append(paragraph);
  }

  function normalizeEditorRows(root, editor) {
    const rows = normalizeProbabilities(readRows(editor));
    rows.forEach((row, rowIndex) => {
      row.forEach((value, columnIndex) => {
        const input = root.querySelector(`[data-row-index="${rowIndex}"] input[data-column-index="${columnIndex}"]`);
        input.value = value.toFixed(3);
      });
    });
    updateRowSums(editor);
  }

  async function initRunner(root) {
    const fixtureUrl = root.dataset.fixtureUrl || "examples/document-triage/demo_cases.json";
    const response = await fetch(fixtureUrl);
    if (!response.ok) {
      throw new Error(`Could not load demo fixture: ${fixtureUrl}`);
    }
    const fixture = await response.json();
    const labels = fixture.labels;
    let scenario = fixture.scenarios[0];

    const select = root.querySelector("[data-scenario-select]");
    const scenarioButtons = root.querySelector("[data-scenario-buttons]");
    const context = root.querySelector("[data-scenario-context]");
    const editor = root.querySelector("[data-matrix-editor]");
    const output = root.querySelector("[data-diagnostic-output]");
    const explanation = root.querySelector("[data-human-explanation]");
    const payload = root.querySelector("[data-payload-output]");
    let variationCounter = 0;

    fixture.scenarios.forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = item.name;
      select.append(option);
    });

    function renderScenario(nextScenario) {
      scenario = nextScenario;
      variationCounter = 0;
      select.value = scenario.id;
      renderScenarioButtons(scenarioButtons, fixture.scenarios, scenario, renderScenario);
      renderContext(context, scenario);
      renderMatrixEditor(editor, labels, scenario.observations);
      runDiagnostic();
    }

    function runDiagnostic() {
      const rows = readRows(editor);
      updateRowSums(editor);
      const diagnostic = diagnoseProbabilityCloud(rows, labels);
      renderOutput(output, labels, diagnostic);
      renderExplanation(explanation, scenario, diagnostic);
      renderPayload(payload, scenario, labels, rows);
    }

    select.addEventListener("change", () => {
      const selected = fixture.scenarios.find((item) => item.id === select.value);
      renderScenario(selected || fixture.scenarios[0]);
    });

    editor.addEventListener("input", () => {
      updateRowSums(editor);
    });

    root.querySelector("[data-run-diagnostic]").addEventListener("click", runDiagnostic);
    root.querySelector("[data-reset-scenario]").addEventListener("click", () => renderScenario(scenario));
    root.querySelector("[data-normalize-rows]").addEventListener("click", () => {
      normalizeEditorRows(root, editor);
      runDiagnostic();
    });
    root.querySelector("[data-generate-variation]").addEventListener("click", () => {
      variationCounter += 1;
      renderMatrixEditor(editor, labels, generateVariationRows(scenario.observations, scenario.expected_state, variationCounter));
      runDiagnostic();
    });

    renderScenario(scenario);
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-dpga-demo-runner]").forEach((root) => {
      initRunner(root).catch((error) => {
        root.textContent = "The live diagnostic workspace could not load. The static examples below are still available.";
        console.error(error);
      });
    });
  });
})();
