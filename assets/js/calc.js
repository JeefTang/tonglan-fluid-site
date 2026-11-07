/* Zero Carbon Assistant — pump sizing & energy calculator (client-side, no data leaves the browser) */
(function () {
  var G = 9.81;

  function num(id) {
    var v = parseFloat((document.getElementById(id) || {}).value);
    return isFinite(v) && v > 0 ? v : 0;
  }
  function fmt(x, d) {
    d = d === undefined ? 1 : d;
    if (!isFinite(x)) return "—";
    return x.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function set(id, text) {
    var el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  /* ---------- Tab 1: energy & payback ---------- */
  function calcEnergy() {
    var Q = num("e_q");          // m3/h
    var H = num("e_h");          // m
    var rho = num("e_rho") || 1000;
    var effNew = (num("e_eff") || 90) / 100;
    var effOld = (num("e_eff_old") || 40) / 100;
    var hours = num("e_hours") || 8000;
    var price = num("e_price") || 0.08;
    var capex = num("e_capex") || 0;

    // hydraulic power kW = rho*g*Q*H / 3.6e6  (Q in m3/h)
    var ph = (rho * G * Q * H) / 3600000;
    var pNew = ph / effNew;
    var pOld = ph / effOld;

    var kwhNew = pNew * hours;
    var kwhOld = pOld * hours;
    var costNew = kwhNew * price;
    var costOld = kwhOld * price;
    var save = costOld - costNew;
    var payback = save > 0 ? capex / save : NaN;
    var co2 = (kwhOld - kwhNew) * 0.000581; // tCO2e, China grid factor ~0.581 kg/kWh

    set("o_ph", fmt(ph, 1) + " kW");
    set("o_pnew", fmt(pNew, 1) + " kW");
    set("o_pold", fmt(pOld, 1) + " kW");
    set("o_kwh", fmt(kwhNew, 0) + " kWh");
    set("o_cost", "$" + fmt(costNew, 0));
    set("o_save", "$" + fmt(save, 0));
    set("o_payback", isFinite(payback) ? fmt(payback, 1) + " years" : "—");
    set("o_co2", fmt(co2, 0) + " t CO₂e/yr");

    var hint = document.getElementById("e_hint");
    if (hint) {
      if (!Q || !H) hint.textContent = "Enter flow and head to see results.";
      else if (save <= 0) hint.textContent = "New-pump efficiency must exceed the existing pump for a saving.";
      else hint.textContent = "Saving is vs. an existing pump at " + fmt(effOld * 100, 0) + "% efficiency.";
    }
  }

  /* ---------- Tab 2: slurry check ---------- */
  function calcSlurry() {
    var Q = num("s_q");
    var H = num("s_h");
    var cw = (num("s_c")) / 100;          // solids concentration by weight
    var sg = num("s_sg") || 2.7;          // solids specific gravity
    var eff = (num("s_eff") || 83) / 100;
    var hours = num("s_hours") || 8000;
    var price = num("s_price") || 0.08;

    // mixture density from solids mass fraction (water SG = 1)
    var cwSafe = Math.min(Math.max(cw, 0), 0.85);
    var rhoMix = 1 / ((cwSafe / sg) + ((1 - cwSafe) / 1)) * 1000; // kg/m3
    var ph = (rhoMix * G * Q * H) / 3600000;
    var shaft = ph / eff;
    var kwh = shaft * hours;
    var cost = kwh * price;

    set("o_mix", fmt(rhoMix, 0) + " kg/m³");
    set("o_sg_mix", fmt(rhoMix / 1000, 2));
    set("o_sph", fmt(ph, 1) + " kW");
    set("o_sshaft", fmt(shaft, 1) + " kW");
    set("o_skwh", fmt(kwh, 0) + " kWh/yr");
    set("o_scost", "$" + fmt(cost, 0) + "/yr");

    var rec = document.getElementById("s_rec");
    if (rec) {
      if (!Q) { rec.textContent = "Enter flow to see the model recommendation."; }
      else if (Q >= 100 && Q <= 400 && H <= 150) {
        rec.textContent = "Fits the V5 vertical five-plunger slurry pump range (100–400 m³/h, ≤150 m head).";
      } else if (Q >= 40 && Q <= 800) {
        rec.textContent = "Outside the V5 slurry envelope — check the multi-plunger high-pressure range (40–800 m³/h, 4–50 MPa).";
      } else {
        rec.textContent = "Outside standard ranges — send us the duty point and we will engineer a custom unit.";
      }
    }
  }

  /* ---------- tabs ---------- */
  function initTabs() {
    var tabs = document.querySelectorAll("[data-tab]");
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        var name = t.getAttribute("data-tab");
        document.querySelectorAll("[data-tab]").forEach(function (x) {
          x.classList.toggle("active", x === t);
        });
        document.querySelectorAll("[data-panel]").forEach(function (p) {
          p.style.display = p.getAttribute("data-panel") === name ? "" : "none";
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTabs();
    ["e_q", "e_h", "e_rho", "e_eff", "e_eff_old", "e_hours", "e_price", "e_capex"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener("input", calcEnergy);
    });
    ["s_q", "s_h", "s_c", "s_sg", "s_eff", "s_hours", "s_price"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener("input", calcSlurry);
    });
    if (document.getElementById("e_q")) calcEnergy();
    if (document.getElementById("s_q")) calcSlurry();
  });
})();
