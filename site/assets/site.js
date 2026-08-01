(() => {
  "use strict";

  const model = document.querySelector(".architecture-model");
  const transcript = document.querySelector(".transcript");
  if (!model || !transcript) return;

  const trace = document.createElement("aside");
  trace.className = "reading-trace";
  trace.setAttribute("data-reading-trace", "enhanced");
  trace.setAttribute("aria-label", "Optional reading trace");
  trace.innerHTML = [
    "<h3>Optional reading trace</h3>",
    "<p id=\"trace-status\" role=\"status\">Static transcript is available above. This optional trace stays in this page only.</p>",
    "<ol aria-label=\"Trace events\"></ol>",
    "<div class=\"trace-actions\">",
    "<button type=\"button\" data-trace-replay>Replay transcript</button>",
    "<button type=\"button\" data-trace-reset>Reset trace</button>",
    "</div>",
  ].join("");
  transcript.insertAdjacentElement("afterend", trace);

  const events = trace.querySelector("ol");
  const status = trace.querySelector("#trace-status");
  const replay = trace.querySelector("[data-trace-replay]");
  const reset = trace.querySelector("[data-trace-reset]");

  const record = (message) => {
    const item = document.createElement("li");
    item.textContent = message;
    events.append(item);
    status.textContent = message;
  };

  record("Trace ready. The complete transcript remains usable without this enhancement.");

  transcript.addEventListener("toggle", () => {
    record(transcript.open ? "Transcript opened." : "Transcript collapsed.");
  });

  replay.addEventListener("click", () => {
    transcript.open = true;
    transcript.scrollIntoView({ behavior: "smooth", block: "start" });
    transcript.querySelector("summary").focus({ preventScroll: true });
    record("Replay returned focus to the static transcript.");
  });

  reset.addEventListener("click", () => {
    events.replaceChildren();
    record("Trace reset. The static transcript was not changed.");
  });
})();
