/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from "react";
import {
  Activity,
  Shield,
  HeartPulse,
  SlidersHorizontal,
  Sparkles,
  Download,
  Terminal,
  Grid,
  Settings,
  HelpCircle,
  Menu,
  ChevronRight,
  ArrowRight,
  TrendingUp,
  AlertTriangle,
  Lock,
  Compass,
  FileSpreadsheet,
  RefreshCw,
  Users
} from "lucide-react";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ZAxis
} from "recharts";

import { PageId, DashboardFilters, OperationsRecord, IncidentRecord } from "./types";
import { STADIUMS, PHASES, ZONE_TYPES, MATCH_CATEGORIES, YEARS, opsTable, incTable } from "./data/mockData";
import { PageHeader } from "./components/PageHeader";
import { KPICard } from "./components/KPICards";
import { AIIntelligence } from "./components/AIIntelligence";
import { AskAIPanel } from "./components/AskAIPanel";

export default function App() {
  const [activePage, setActivePage] = useState<PageId>("Intro");
  const [sidebarWidth, setSidebarWidth] = useState<number>(265);
  const isResizing = useRef<boolean>(false);

  // Filter States
  const [selectedStadiums, setSelectedStadiums] = useState<string[]>(STADIUMS);
  const [selectedPhases, setSelectedPhases] = useState<string[]>(PHASES);
  const [selectedYears, setSelectedYears] = useState<number[]>(YEARS);
  const [selectedZones, setSelectedZones] = useState<string[]>(ZONE_TYPES);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(MATCH_CATEGORIES);

  // Helper selectors toggler
  const [allStadChecked, setAllStadChecked] = useState(true);
  const [allPhaseChecked, setAllPhaseChecked] = useState(true);

  // ── Drag sidebar Resize Handler ──
  const startResize = (e: React.MouseEvent) => {
    e.preventDefault();
    isResizing.current = true;
    document.addEventListener("mousemove", handleResize);
    document.addEventListener("mouseup", stopResize);
  };

  const handleResize = (e: MouseEvent) => {
    if (!isResizing.current) return;
    const nextWidth = Math.min(420, Math.max(215, e.clientX));
    setSidebarWidth(nextWidth);
  };

  const stopResize = () => {
    isResizing.current = false;
    document.removeEventListener("mousemove", handleResize);
    document.removeEventListener("mouseup", stopResize);
  };

  // Toggle checks utility
  const toggleAllStadiums = () => {
    if (allStadChecked) {
      setSelectedStadiums([]);
    } else {
      setSelectedStadiums(STADIUMS);
    }
    setAllStadChecked(!allStadChecked);
  };

  const toggleAllPhases = () => {
    if (allPhaseChecked) {
      setSelectedPhases([]);
    } else {
      setSelectedPhases(PHASES);
    }
    setAllPhaseChecked(!allPhaseChecked);
  };

  // ── FILTER DATA DYNAMICALLY ──
  const filteredData = opsTable.filter((row) => {
    return (
      selectedStadiums.includes(row.stadium_name) &&
      selectedPhases.includes(row.phase) &&
      selectedYears.includes(row.season_year) &&
      selectedZones.includes(row.zone_type) &&
      selectedCategories.includes(row.match_category)
    );
  });

  const filteredIncidents = incTable.filter((row) => {
    return (
      selectedStadiums.includes(row.stadium_name) &&
      selectedYears.includes(row.season_year)
    );
  });

  // Safe checks if empty
  const isDataAvailable = filteredData.length > 0;

  // ── COMPUTE METRIC AGGREGATES (KPI calculations matching Streamlit) ──
  const totalPeopleSum = filteredData.reduce((acc, curr) => acc + curr.people_count, 0);
  const averageOccupancy = isDataAvailable 
    ? filteredData.reduce((acc, curr) => acc + curr.occupancy_rate, 0) / filteredData.length 
    : 0;
  
  const averageQueueWait = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.avg_queue_wait_time, 0) / filteredData.length
    : 0;

  const averageAmbulanceResponse = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.ambulance_response_time, 0) / filteredData.length
    : 0;

  const overallRiskScore = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.risk_score, 0) / filteredData.length
    : 0;

  const medicalIncidentCount = filteredData.reduce((acc, curr) => acc + curr.medical_incidents, 0);
  const medicalIncidentRatePer1K = totalPeopleSum > 0 ? (medicalIncidentCount / totalPeopleSum) * 1000 : 0;

  const averageHeatRisk = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.heat_risk_index, 0) / filteredData.length
    : 0;

  const overallCrowdPressure = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.occupancy_rate * 80 * (0.8 + Math.random() * 0.1), 0) / filteredData.length
    : 0;

  const averageBottleneckRisk = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.avg_queue_wait_time * 2.2, 0) / filteredData.length
    : 0;

  // Count capacity breaches (General thresholds)
  const capacityBreachCount = filteredData.filter((r) => r.occupancy_rate >= 0.55).length;
  const capacityBreachRatio = isDataAvailable ? (capacityBreachCount / filteredData.length) * 100 : 0;

  // Resolution rate
  const resolvedIncCount = filteredIncidents.filter((i) => i.status === "Resolved").length;
  const incidentResolutionRate = filteredIncidents.length > 0
    ? (resolvedIncCount / filteredIncidents.length) * 100
    : 0;

  // Security aggregates
  const totalUnauthorized = filteredData.reduce((acc, curr) => acc + curr.unauthorized_entry_attempts, 0);
  const totalCounterfeit = filteredData.reduce((acc, curr) => acc + curr.counterfeit_ticket_cases, 0);
  const totalPitchInvasions = filteredData.reduce((acc, curr) => acc + curr.pitch_invasion_attempt, 0);
  const totalEjections = filteredData.reduce((acc, curr) => acc + curr.fan_ejections, 0);

  // Critical/Monitor count
  const criticalVolume = filteredData.filter((r) => r.risk_band === "Critical").length;
  const monitorVolume = filteredData.filter((r) => r.risk_band === "Monitor").length;

  // Resource planning aggregates
  const totalRequiredStaff = filteredData.reduce((acc, curr) => acc + curr.required_staff, 0);
  const totalBarricades = filteredData.reduce((acc, curr) => acc + curr.required_barricades, 0);
  const totalParamedicTeams = filteredData.reduce((acc, curr) => acc + curr.deployed_medical_teams, 0);

  const averageStaffRatio = isDataAvailable
    ? filteredData.reduce((acc, curr) => acc + curr.staff_adequacy_ratio, 0) / filteredData.length
    : 0;

  // Build current context text summary for the AI engine
  const contextSummaryText = `
[IPL STADIUM SAFETY TELEMETRY]
Filtered Stadiums: ${selectedStadiums.join(", ")}
Years Checked: ${selectedYears.join(", ")}
Phases: ${selectedPhases.join(", ")}

Operational Metrics:
- Overall advanced risk index: ${overallRiskScore.toFixed(2)} / 100
- Mean queue waiting duration: ${averageQueueWait.toFixed(1)} mins
- Paramedical response lag: ${averageAmbulanceResponse.toFixed(1)} mins
- Crowd pressure index average: ${overallCrowdPressure.toFixed(1)} %
- Bottleneck risk level: ${averageBottleneckRisk.toFixed(1)} %
- Thermal risk factor index: ${averageHeatRisk.toFixed(1)}
- Capacity loading boundary breach levels: ${capacityBreachRatio.toFixed(1)}% of stadium zones
- Incident containment resolution factor: ${incidentResolutionRate.toFixed(1)}%

Criticality summary:
- Zones marked CRITICAL safety threat: ${criticalVolume}
- Zones marked MONITOR/ALERT level: ${monitorVolume}

Security parameters:
- Boundary ingress attempts flagged: ${totalUnauthorized}
- Illegal ticket cases reported: ${totalCounterfeit}
- Core pitch breaches stopped: ${totalPitchInvasions}
- Spectator ejections: ${totalEjections}

Resources:
- Deployed operations staff: ${totalRequiredStaff} personnel
- Temporary crowd control fences required: ${totalBarricades} units
- Deployed emergency response units: ${totalParamedicTeams} teams
- Warden density ratio: ${averageStaffRatio.toFixed(2)} per thousand spectator units
  `;

  // Download filtered data as CSV (simple client side generator)
  const downloadCSV = () => {
    let csvContent = "data:text/csv;charset=utf-8,";
    // Header
    csvContent += "Stadium,Phase,Year,Zone Type,People Count,Occupancy,Queue Wait,Ambulance Response,Risk Score,Risk Band,Action\n";
    
    // Rows
    filteredData.forEach((row) => {
      csvContent += `"${row.stadium_name}","${row.phase}",${row.season_year},"${row.zone_type}",${row.people_count},${row.occupancy_rate},${row.avg_queue_wait_time},${row.ambulance_response_time},${row.risk_score},"${row.risk_band}","${row.recommended_action}"\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `ipl_crowd_safety_telemetry_${activePage.toLowerCase().replace(/ /g, "_")}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans relative">
      {/* ── DRAGGABLE SIDEBAR PANEL ── */}
      <aside
        style={{ width: `${sidebarWidth}px` }}
        className="h-full bg-slate-900 border-r border-slate-800 flex flex-col flex-shrink-0 relative overflow-hidden transition-all duration-75 select-none"
      >
        {/* Decorative branding top bar */}
        <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-violet-500 via-indigo-500 to-teal-400" />
        
        {/* Header brand logo */}
        <div className="p-6 text-center border-b border-slate-800/80 flex flex-col items-center">
          <div className="text-3xl filter drop-shadow-[0_0_10px_rgba(167,139,250,0.4)] mb-1">🏏</div>
          <h2 className="text-sm font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-violet-300 via-indigo-200 to-teal-200 font-sans uppercase">
            IPL Crowd Safety
          </h2>
          <div className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mt-1">
            Stadium Operations Control
          </div>
        </div>

        {/* Sidebar menu content scrollbar */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Navigation Category */}
          <div className="space-y-1">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-2 mb-2 block">
              DASHBOARD MODULES
            </span>
            {[
              { id: "Intro", label: "Intro", icon: "🚀", desc: "Platform Welcome & Portal" },
              { id: "Overview", label: "Overview", icon: "🏠", desc: "Executive Master Dashboard" },
              { id: "Crowd Flow", label: "Crowd Flow", icon: "🌊", desc: "Spectator Density & Bottlenecks" },
              { id: "Medical & Heat", label: "Medical & Heat", icon: "🏥", desc: "Emergency Response & Thermal Index" },
              { id: "Security", label: "Security Portal", idMap: "Security", icon: "🔒", desc: "Perimeter Activity Logs" },
              { id: "Resource Planning", label: "Resource Planner", idMap: "Resource Planning", icon: "📦", desc: "Staffing & Infrastructure Allocation" },
              { id: "Risk Matrix", label: "Risk Matrix", icon: "🚨", desc: "Critical Hazard Decision Charts" },
              { id: "Ask AI", label: "Ask AI Assistant", idMap: "Ask AI", icon: "💬", desc: "Operations Chat Partner" }
            ].map((item) => {
              const targetPageId = (item.idMap || item.id) as PageId;
              const isActive = activePage === targetPageId;
              return (
                <button
                  key={item.id}
                  onClick={() => setActivePage(targetPageId)}
                  className={`w-full text-left p-3 rounded-xl transition-all duration-200 flex items-center gap-3 relative cursor-pointer ${isActive ? "bg-indigo-600/15 border border-indigo-500/30 text-indigo-200" : "hover:bg-slate-800/50 border border-transparent text-slate-400 hover:text-slate-200"}`}
                >
                  <span className="text-lg flex-shrink-0">{item.icon}</span>
                  <div className="min-w-0">
                    <div className="text-xs font-bold leading-none">{item.label}</div>
                    <div className="text-[9px] text-slate-500 truncate mt-1 font-light leading-none">{item.desc}</div>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Dynamic Sidebar Filters - Only visible if not on Intro home page */}
          {activePage !== "Intro" && (
            <div className="pt-4 border-t border-slate-800/80 space-y-5">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-2 block">
                FILTER PLATFORM DATA
              </span>

              {/* Stadium Checkboxes */}
              <div className="space-y-1.5 pl-1.5">
                <div className="flex items-center justify-between text-xs text-slate-400 font-bold mb-1">
                  <span>Stadium Venues</span>
                  <button
                    onClick={toggleAllStadiums}
                    className="text-[10px] text-violet-400 hover:text-violet-300 font-semibold cursor-pointer"
                  >
                    {allStadChecked ? "Clear All" : "Select All"}
                  </button>
                </div>
                <div className="max-h-24 overflow-y-auto space-y-1 pr-1 border border-slate-800 bg-slate-950/20 p-2 rounded-lg">
                  {STADIUMS.map((stadium) => {
                    const isChecked = selectedStadiums.includes(stadium);
                    return (
                      <label key={stadium} className="flex items-center gap-2 text-[10px] text-slate-400 hover:text-slate-300 select-none cursor-pointer">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {
                            if (isChecked) {
                              setSelectedStadiums(selectedStadiums.filter((s) => s !== stadium));
                            } else {
                              setSelectedStadiums([...selectedStadiums, stadium]);
                            }
                          }}
                          className="rounded text-indigo-600 border-slate-800 bg-slate-900 focus:ring-0 cursor-pointer"
                        />
                        <span className="truncate">{stadium.split(" (")[0]}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              {/* Phase Checkboxes */}
              <div className="space-y-1.5 pl-1.5">
                <div className="flex items-center justify-between text-xs text-slate-400 font-bold mb-1">
                  <span>Match Phase</span>
                  <button
                    onClick={toggleAllPhases}
                    className="text-[10px] text-violet-400 hover:text-violet-300 font-semibold cursor-pointer"
                  >
                    {allPhaseChecked ? "Clear" : "All"}
                  </button>
                </div>
                <div className="max-h-24 overflow-y-auto space-y-1 pr-1 border border-slate-800 bg-slate-950/20 p-2 rounded-lg">
                  {PHASES.map((phase) => {
                    const isChecked = selectedPhases.includes(phase);
                    return (
                      <label key={phase} className="flex items-center gap-2 text-[10px] text-slate-400 hover:text-slate-300 select-none cursor-pointer">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {
                            if (isChecked) {
                              setSelectedPhases(selectedPhases.filter((p) => p !== phase));
                            } else {
                              setSelectedPhases([...selectedPhases, phase]);
                            }
                          }}
                          className="rounded text-indigo-600 border-slate-800 bg-slate-900 focus:ring-0 cursor-pointer"
                        />
                        <span className="truncate">{phase}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              {/* Year Multiple Checklist */}
              <div className="space-y-1 pl-1.5">
                <span className="text-xs text-slate-400 font-bold block mb-1">Operational Year</span>
                <div className="flex gap-2">
                  {YEARS.map((yr) => {
                    const isChecked = selectedYears.includes(yr);
                    return (
                      <button
                        key={yr}
                        onClick={() => {
                          if (isChecked) {
                            setSelectedYears(selectedYears.filter((y) => y !== yr));
                          } else {
                            setSelectedYears([...selectedYears, yr]);
                          }
                        }}
                        className={`text-center py-1 flex-1 rounded-lg text-[10px] font-bold border cursor-pointer transition-all ${isChecked ? "bg-indigo-600/30 border-indigo-500 text-indigo-300" : "bg-slate-850 border-slate-800 text-slate-500 hover:text-slate-300"}`}
                      >
                        {yr}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Zone Type Multiple checklist */}
              <div className="space-y-1 pl-1.5">
                <span className="text-xs text-slate-400 font-bold block mb-1">Zone Divisions</span>
                <div className="max-h-24 overflow-y-auto space-y-1 pr-1 border border-slate-800 bg-slate-950/20 p-2 rounded-lg">
                  {ZONE_TYPES.map((zt) => {
                    const isChecked = selectedZones.includes(zt);
                    return (
                      <label key={zt} className="flex items-center gap-2 text-[10px] text-slate-300 select-none cursor-pointer">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {
                            if (isChecked) {
                              setSelectedZones(selectedZones.filter((z) => z !== zt));
                            } else {
                              setSelectedZones([...selectedZones, zt]);
                            }
                          }}
                          className="rounded text-indigo-600 border-slate-800 bg-slate-900 focus:ring-0 cursor-pointer"
                        />
                        <span className="truncate">{zt}</span>
                      </label>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar Resize Handle on the right edge */}
        <div
          onMouseDown={startResize}
          className="absolute top-0 right-0 w-[4px] h-full cursor-col-resize hover:bg-violet-600/40 transition-colors select-none group flex items-center justify-center"
        >
          <div className="w-[1px] h-10 bg-slate-800 group-hover:bg-violet-500 opacity-60 pointer-events-none" />
        </div>
      </aside>

      {/* ── MAIN WORKSPACE CONTENT WINDOW ── */}
      <main className="flex-1 h-full overflow-y-auto bg-slate-950 p-6 md:p-8 flex flex-col space-y-6">
        {/* Header Alert if filtered is empty */}
        {!isDataAvailable && activePage !== "Intro" ? (
          <div className="p-16 bg-slate-900 border border-slate-800 rounded-3xl flex flex-col items-center justify-center text-center space-y-4 max-w-3xl mx-auto shadow-2xl">
            <AlertTriangle className="w-16 h-16 text-amber-500 animate-bounce" />
            <h3 className="text-lg font-bold text-slate-100">Filtered Dataset is Empty</h3>
            <p className="text-xs text-slate-400 max-w-md">
              No matching records conform to the currently highlighted dashboard choices. Please select supplementary Stadiums, Phase periods or Zones in the sidebar.
            </p>
            <button
              onClick={() => {
                setSelectedStadiums(STADIUMS);
                setSelectedPhases(PHASES);
                setSelectedYears(YEARS);
                setSelectedZones(ZONE_TYPES);
                setSelectedCategories(MATCH_CATEGORIES);
              }}
              className="py-2 px-6 bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-xl text-xs font-semibold cursor-pointer shadow-lg active:scale-95 transition-all"
            >
              Reset Filters to Default
            </button>
          </div>
        ) : (
          <>
            {/* ═══════════════════════════════════════════════════════════
                PAGE 0 — INTRO (Platform oriented welcoming center)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Intro" && (
              <div className="max-w-6xl mx-auto space-y-8 animate-fadeIn py-4">
                {/* Visual Intro Hero: Comfortable Slate Midnight Theme (In-between light and very deep purple) */}
                <div className="relative p-10 md:p-14 rounded-3xl bg-slate-900 border border-slate-800/80 shadow-2xl overflow-hidden shadow-indigo-950/20 text-center">
                  <div className="absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r from-violet-500 via-indigo-500 to-teal-400" />
                  
                  {/* Glowing background circles for visual depth */}
                  <div className="absolute -top-24 -left-24 w-80 h-80 bg-violet-600/10 rounded-full blur-3xl pointer-events-none" />
                  <div className="absolute -bottom-24 -right-24 w-80 h-80 bg-teal-500/5 rounded-full blur-3xl pointer-events-none" />

                  <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-violet-500/10 border border-violet-500/30 rounded-full text-[10px] text-violet-400 font-bold uppercase tracking-widest mb-6 animate-pulse select-none">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Executive Analytics Suite</span>
                  </div>

                  <h1 className="text-4xl md:text-5xl font-black tracking-tight text-white leading-tight font-sans">
                    IPL Stadium Crowd Safety<br />
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-indigo-300 to-teal-300">
                      Operations Management Dashboard
                    </span>
                  </h1>

                  <p className="mt-4 text-xs md:text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed font-light">
                    An advanced professional platform specifically engineered for stadium safety units, operations directors, and incident response personnel to inspect, forecast, and counter crowding risks in IPL tournaments.
                  </p>

                  {/* Summary Core counts */}
                  <div className="flex flex-wrap justify-center gap-4 md:gap-6 mt-8">
                    {[
                      { val: opsTable.length.toLocaleString(), lbl: "Operations Records" },
                      { val: STADIUMS.length.toString(), lbl: "High Capacity Stadiums" },
                      { val: ZONE_TYPES.length.toString(), lbl: "Monitored Subsections" },
                      { val: YEARS.length.toString(), lbl: "Captured Seasons" }
                    ].map((stat, i) => (
                      <div key={i} className="py-3 px-5 rounded-2xl bg-slate-950/50 border border-slate-800/80 min-w-[120px] backdrop-blur-md">
                        <span className="text-2xl font-black text-violet-400 block font-sans">
                          {stat.val}
                        </span>
                        <span className="text-[9px] font-bold text-slate-500 uppercase tracking-wider block mt-1">
                          {stat.lbl}
                        </span>
                      </div>
                    ))}
                  </div>

                  {/* Trigger call */}
                  <div className="mt-10 flex justify-center">
                    <button
                      onClick={() => setActivePage("Overview")}
                      className="py-3 px-8 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg hover:shadow-violet-500/25 cursor-pointer active:scale-95 transition-all flex items-center gap-2 group"
                    >
                      <span>Explore Command Panel</span>
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </button>
                  </div>
                </div>

                {/* Highly descriptive introductions to other pages */}
                <div className="space-y-4">
                  <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500 text-center">
                    Core Dashboard Modules
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[
                      { icon: "🏠", bg: "hover:border-violet-500/30", label: "Overview", desc: "The master control center compiling critical hazard parameters, density matrices, paramedic response speeds, and match safety ratings into an executive summary deck.", id: "Overview" },
                      { icon: "🌊", bg: "hover:border-indigo-500/30", label: "Crowd Flow", desc: "A detailed spectator flow and physical bottleneck risk analyzer. Maps queue wait times, perimeter loading rates, and crowd stress benchmarks.", id: "Crowd Flow" },
                      { icon: "🏥", bg: "hover:border-emerald-500/30", label: "Medical & Heat", desc: "Emergency medical and weather telemetry module. Tracks local hydration risk indicators, ambient thermal loads, and ambulance readiness indices.", id: "Medical & Heat" },
                      { icon: "🔒", bg: "hover:border-rose-500/30", label: "Security", desc: "Access safety and intrusion logging. Collects boundary violation attempts, duplicate ticket counts, spectator ejections, and overall gate safety breaches.", id: "Security" },
                      { icon: "📦", bg: "hover:border-teal-500/30", label: "Resource Planner", desc: "Allocates operational staff, temporary steel boundaries, and medical squads efficiently relative to the current match risk rating.", id: "Resource Planning" },
                      { icon: "🚨", bg: "hover:border-red-500/30", label: "Risk Matrix", desc: "Our prioritized decision-support grid. Leverages weighted safety algorithms to isolate and rank high threat hotspot zones instantly.", id: "Risk Matrix" },
                      { icon: "💬", bg: "hover:border-indigo-600/30", label: "Ask AI", desc: "An intelligent conversational chatbot partner powered by Gemini. Formulate direct, natural questions to query emergency response guides.", id: "Ask AI" }
                    ].map((mod, i) => (
                      <button
                        key={i}
                        onClick={() => setActivePage(mod.id as PageId)}
                        className={`text-left p-5 bg-slate-900 border border-slate-800 rounded-2xl block space-y-2 cursor-pointer transition-all duration-300 hover:-translate-y-1 hover:bg-slate-900/80 hover:shadow-xl ${mod.bg}`}
                      >
                        <span className="text-2xl block">{mod.icon}</span>
                        <div className="text-xs font-extrabold text-slate-200 uppercase tracking-wide">
                          {mod.label}
                        </div>
                        <p className="text-[11px] text-slate-400 font-light leading-relaxed">
                          {mod.desc}
                        </p>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Tech Stack and design credentials */}
                <div className="pt-6 text-center border-t border-slate-800/80 flex flex-col items-center gap-3">
                  <div className="flex flex-wrap justify-center gap-2">
                    {["React 19", "Express.js Backend", "Tailwind CSS", "Recharts Visualization", "Gemini 3.5 Operational API"].map((tech) => (
                      <span key={tech} className="px-3 py-1 bg-slate-900/60 border border-slate-850 rounded-full text-[10px] text-slate-400 font-medium">
                        {tech}
                      </span>
                    ))}
                  </div>
                  <p className="text-[10px] text-slate-600 font-light max-w-sm">
                    IPL Crowd Safety Control Suite • Engineered with precision data paradigms for professional stadium command teams.
                  </p>
                </div>
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 1 — OVERVIEW (Master commanding deck)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Overview" && (
              <div className="space-y-6">
                <PageHeader
                  icon="🏠"
                  title="IPL Stadium Operations Master Command Dashboard"
                  subtitle="Executive aggregate monitoring, security alerts, ambulance dispatch and resource deployment summaries"
                />

                {/* Focused Center KPI Cards */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <KPICard label="Overall Risk Score" value={overallRiskScore.toFixed(2)} type="crit" sub="Advanced combined score" />
                  <KPICard label="Medical Incident Rate" value={`${medicalIncidentRatePer1K.toFixed(2)}/1K`} type="warn" sub="Incidents per 1K spectators" />
                  <KPICard label="Capacity Breach" value={`${capacityBreachRatio.toFixed(1)}%`} type="info" sub="Monitored zones above limit" />
                  <KPICard label="Resolution Rate" value={`${incidentResolutionRate.toFixed(1)}%`} type="ok" sub="Resolved incident percentage" />
                  <KPICard label="Ambulance Response" value={`${averageAmbulanceResponse.toFixed(1)} min`} type="warn" sub="Average dispatch to arrival lag" />
                </div>

                {/* Recharts Visualizations Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Left Column: Trending charts */}
                  <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Operational Risk Trend across Match Phases
                    </h4>
                    <div className="h-[280px] w-full">
                      {/* Formatted dataset for LineChart */}
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={PHASES.map((ph) => {
                            const phaseRows = filteredData.filter((r) => r.phase === ph);
                            const avgRisk = phaseRows.length > 0 
                              ? phaseRows.reduce((a, b) => a + b.risk_score, 0) / phaseRows.length 
                              : 0;
                            return { name: ph, "Risk Score": parseFloat(avgRisk.toFixed(1)) };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} domain={[0, 100]} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Line type="monotone" dataKey="Risk Score" stroke="#8b5cf6" strokeWidth={3} activeDot={{ r: 8 }} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Mini Pie layout */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                      <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                        Zone Risk Band Splitting
                      </h4>
                      <div className="h-[180px] w-full flex items-center justify-center">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={[
                                { name: "Critical", value: criticalVolume, color: "#ef4444" },
                                { name: "Monitor", value: monitorVolume, color: "#f59e0b" },
                                { name: "Safe", value: Math.max(0, filteredData.length - criticalVolume - monitorVolume), color: "#10b981" }
                              ]}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={80}
                              paddingAngle={5}
                              dataKey="value"
                            >
                              {[
                                { color: "#ef4444" },
                                { color: "#f59e0b" },
                                { color: "#10b981" }
                              ].map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                              ))}
                            </Pie>
                            <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                    {/* Foot legend labels */}
                    <div className="grid grid-cols-3 text-center border-t border-slate-800 pt-3 text-[10px] text-slate-400 font-bold">
                      <div>
                        <div className="text-rose-500 font-black text-base">{criticalVolume}</div>
                        Critical
                      </div>
                      <div>
                        <div className="text-amber-500 font-black text-base">{monitorVolume}</div>
                        Monitor
                      </div>
                      <div>
                        <div className="text-emerald-500 font-black text-base">
                          {Math.max(0, filteredData.length - criticalVolume - monitorVolume)}
                        </div>
                        Safe
                      </div>
                    </div>
                  </div>
                </div>

                {/* Sub Bar visual row */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Match Category Densities in Dataset
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={MATCH_CATEGORIES.map((cat) => ({
                            name: cat.split(" ")[0] + " Match",
                            "Record Count": filteredData.filter((r) => r.match_category === cat).length
                          }))}
                          layout="vertical"
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis type="number" stroke="#64748b" fontSize={10} />
                          <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={10} width={80} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar dataKey="Record Count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Average Advanced Risk Score by Zone Division
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={ZONE_TYPES.map((zt) => {
                            const zRows = filteredData.filter((r) => r.zone_type === zt);
                            const avgR = zRows.length > 0 
                              ? zRows.reduce((a, b) => a + b.risk_score, 0) / zRows.length 
                              : 0;
                            return { name: zt.split(" ")[0], "Avg Risk": parseFloat(avgR.toFixed(1)) };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} domain={[0, 100]} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar dataKey="Avg Risk" fill="#10b981" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* Tabular Telemetry matrices */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
                    <div>
                      <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest">
                        AI Risk Priority Matrix — Top 5 High-hazard Zones
                      </h4>
                      <p className="text-[10px] text-slate-500 mt-1">
                        Weighted hazard model isolates critical stadium sections needing staff or paramedic relocation.
                      </p>
                    </div>
                    {/* Action buttons */}
                    <button
                      onClick={downloadCSV}
                      className="py-1.5 px-4 bg-slate-800 hover:bg-slate-705 border border-slate-700/80 rounded-xl text-xs font-bold text-slate-300 flex items-center gap-1.5 transition-all select-none cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Download Telemetry (.CSV)</span>
                    </button>
                  </div>

                  <div className="overflow-x-auto border border-slate-800 rounded-xl">
                    <table className="w-full text-left border-collapse text-xs font-light">
                      <thead>
                        <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 font-extrabold uppercase tracking-wider text-[10px]">
                          <th className="p-3">Stadium Venue</th>
                          <th className="p-3">Zone Section</th>
                          <th className="p-3">Zone Type</th>
                          <th className="p-3">Phase Period</th>
                          <th className="p-3 text-center">Crowd Count</th>
                          <th className="p-3 text-center">Risk Index</th>
                          <th className="p-3 text-center">Threat Classification</th>
                          <th className="p-3">Recommended Control Task</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/65 text-slate-300">
                        {filteredData
                          .sort((a, b) => b.risk_score - a.risk_score)
                          .slice(0, 5)
                          .map((row, idx) => (
                            <tr key={idx} className="hover:bg-slate-950/40">
                              <td className="p-3 font-semibold truncate max-w-[140px]" title={row.stadium_name}>{row.stadium_name.split(" (")[0]}</td>
                              <td className="p-3">{row.zone_name}</td>
                              <td className="p-3">{row.zone_type}</td>
                              <td className="p-3">{row.phase}</td>
                              <td className="p-3 text-center font-mono">{row.people_count.toLocaleString()}</td>
                              <td className="p-3 text-center font-mono font-bold text-violet-400">{row.risk_score}</td>
                              <td className="p-3 text-center">
                                <span className={`px-2 py-0.5 rounded-full text-[9px] font-extrabold leading-none ${row.risk_band === "Critical" ? "bg-rose-500/15 text-rose-400 border border-rose-500/30" : "bg-amber-500/15 text-amber-400 border border-amber-500/30"}`}>
                                  {row.risk_band}
                                </span>
                              </td>
                              <td className="p-3 text-[11px] text-emerald-400 font-medium italic">{row.recommended_action}</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* ── AI Executive Summary (at bottom of page, no visuals under it) ── */}
                <AIIntelligence summaryText={contextSummaryText} pageName="Overview" />
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 2 — CROWD FLOW (Entrance wait queues and congestion)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Crowd Flow" && (
              <div className="space-y-6">
                <PageHeader
                  icon="🌊"
                  title="Crowd Flow, Gate Congestion & Bottleneck Analyzer"
                  subtitle="In-depth inspection of ticket turnstiles, crowd load trends, queue wait spikes and bottleneck alert lists"
                />

                {/* Flow KPIs */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <KPICard label="Bottleneck Hazard Index" value={averageBottleneckRisk.toFixed(1)} type="crit" sub="Average queue blocking ratio" />
                  <KPICard label="Average Turnstile Wait" value={`${averageQueueWait.toFixed(1)} mins`} type="warn" sub="Average ticket processing delay" />
                  <KPICard label="Total Active Crowd" value={totalPeopleSum.toLocaleString()} type="info" sub="Filtered match spectators count" />
                  <KPICard label="Capacity Load Exceeded" value={`${capacityBreachRatio.toFixed(1)}%`} type="crit" sub="Percentage of zones above safe limit" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Left Column: Spectator count lines across periods */}
                  <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Attendance Loading across Match Phases by Zone Division
                    </h4>
                    <div className="h-[280px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={PHASES.map((ph) => {
                            const phaseData = filteredData.filter((r) => r.phase === ph);
                            const result: any = { name: ph };
                            ZONE_TYPES.forEach((zt) => {
                              const zRows = phaseData.filter((r) => r.zone_type === zt);
                              const totalPeople = zRows.reduce((a, b) => a + b.people_count, 0);
                              result[zt.split(" ")[0]] = totalPeople;
                            });
                            return result;
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Legend />
                          <Line type="monotone" dataKey="General" stroke="#a78bfa" />
                          <Line type="monotone" dataKey="VIP" stroke="#3b82f6" />
                          <Line type="monotone" dataKey="Outer" stroke="#ef4444" />
                          <Line type="monotone" dataKey="Food" stroke="#10b981" />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Flow Wait times Thermal Grid */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                      <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                        Turnstile Delay Index Matrix (Stadium x Phase)
                      </h4>
                      <p className="text-[10px] text-slate-500 mb-3">
                        Lists median wait durations in minutes. Brighter colors indicate severe congestion.
                      </p>
                      
                      <div className="space-y-1 text-xs">
                        {STADIUMS.slice(0, 4).map((stad) => {
                          const miniName = stad.split(" (")[0];
                          return (
                            <div key={stad} className="grid grid-cols-6 gap-0.5 items-center">
                              <div className="text-[10px] font-semibold text-slate-400 truncate pr-1" title={stad}>
                                {miniName.split(" ")[0]}
                              </div>
                              {PHASES.map((ph) => {
                                const matched = filteredData.find((r) => r.stadium_name === stad && r.phase === ph);
                                const waitVal = matched ? matched.avg_queue_wait_time : 0;
                                let heatColor = "bg-slate-900 text-slate-500";
                                if (waitVal >= 25) heatColor = "bg-rose-950 border border-rose-500 text-rose-300 font-bold";
                                else if (waitVal >= 15) heatColor = "bg-amber-950 border border-amber-500 text-amber-300 font-bold";
                                else if (waitVal > 0) heatColor = "bg-indigo-950/60 text-indigo-300";
                                return (
                                  <div
                                    key={ph}
                                    title={`${miniName} - ${ph}: ${waitVal} min wait`}
                                    className={`py-2 text-center text-[10px] font-mono rounded ${heatColor}`}
                                  >
                                    {waitVal}
                                  </div>
                                );
                              })}
                            </div>
                          );
                        })}
                        {/* Headers */}
                        <div className="grid grid-cols-6 gap-0.5 pt-1 text-[8px] font-bold text-slate-500 uppercase tracking-widest text-center border-t border-slate-800 mt-2">
                          <div className="text-left">Venue</div>
                          <div>Pre</div>
                          <div>1st</div>
                          <div>Brk</div>
                          <div>2nd</div>
                          <div>Exit</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Mean Bottleneck Stress Score by Division
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={ZONE_TYPES.map((zt) => {
                            const zRows = filteredData.filter((r) => r.zone_type === zt);
                            const avgB = zRows.length > 0 
                              ? zRows.reduce((a, b) => a + b.avg_queue_wait_time * 2.2, 0) / zRows.length 
                              : 0;
                            return { name: zt.split(" ")[0], "Bottleneck Risk": parseFloat(avgB.toFixed(1)) };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} domain={[0, 100]} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar dataKey="Bottleneck Risk" fill="#ef4444" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Entry Queue waiting Status Breakdown
                    </h4>
                    <div className="h-[180px] w-full">
                      {/* Count categorizations strictly representing queue classifications */}
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={[
                              { name: "Extreme wait (25m+)", value: filteredData.filter((r) => r.avg_queue_wait_time >= 25).length, color: "#ef4444" },
                              { name: "Elevated wait (15-24m)", value: filteredData.filter((r) => r.avg_queue_wait_time >= 15 && r.avg_queue_wait_time < 25).length, color: "#f59e0b" },
                              { name: "Acceptable wait (Under 15m)", value: filteredData.filter((r) => r.avg_queue_wait_time < 15).length, color: "#10b981" }
                            ]}
                            cx="50%"
                            cy="50%"
                            outerRadius={65}
                            fill="#8884d8"
                            dataKey="value"
                            label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                          >
                            {[
                              { color: "#ef4444" },
                              { color: "#f59e0b" },
                              { color: "#10b981" }
                            ].map((entry, idx) => (
                              <Cell key={`cell-${idx}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* ── AI Intelligence (at bottom) ── */}
                <AIIntelligence summaryText={contextSummaryText} pageName="Crowd Flow" />
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 3 — MEDICAL & HEAT (Weather loading and response)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Medical & Heat" && (
              <div className="space-y-6">
                <PageHeader
                  icon="🏥"
                  title="Medical Incident Support & Heat stress Telemetry Room"
                  subtitle="Assessing spectator dehydration risks, temperature loading, ambulance delays and paramedic deployment coordinates"
                />

                {/* Medical KPIs */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <KPICard label="Medical Incident Rate" value={`${medicalIncidentRatePer1K.toFixed(2)}/1K`} type="warn" sub="Incidents per 1K people" />
                  <KPICard label="Ambulance dispatch delay" value={`${averageAmbulanceResponse.toFixed(1)} min`} type="crit" sub="Response Lag" />
                  <KPICard label="Average Heat Index" value={averageHeatRisk.toFixed(1)} type="warn" sub="Temp x Humidity combined load" />
                  <KPICard label="Delayed Medical Zones" value={filteredData.filter((r) => r.ambulance_response_time >= 10).length.toString()} type="crit" sub="Lag >= 10 minutes" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Left Column: Heat Stress levels */}
                  <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Thermal Stress Index trends across Match Phases
                    </h4>
                    <div className="h-[280px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={PHASES.map((ph) => {
                            const pRows = filteredData.filter((r) => r.phase === ph);
                            const avgH = pRows.length > 0 
                              ? pRows.reduce((a, b) => a + b.heat_risk_index, 0) / pRows.length 
                              : 0;
                            return { name: ph, "Thermal Load": parseFloat(avgH.toFixed(1)) };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} domain={[20, 100]} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Line type="monotone" dataKey="Thermal Load" stroke="#e11d48" strokeWidth={3} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Total incidents by Stadium */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Aggregated Medical Cases by Stadium Venue
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={STADIUMS.map((stad) => ({
                            name: stad.split(" Stadium")[0].split(" ").pop(),
                            "Medical Incidents": filteredData.filter((r) => r.stadium_name === stad).reduce((a, b) => a + b.medical_incidents, 0)
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar fill="#f43f5e" dataKey="Medical Incidents" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* Sub details: Scatter block of Heat loads vs Incident quantities */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Dehydration Risk Profile (Local Thermal Stress vs Incident Counts)
                    </h4>
                    <div className="h-[220px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart>
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis type="number" dataKey="heat" name="Thermal Index" stroke="#64748b" fontSize={9} label={{ value: "Heat Index", position: "insideBottom", offset: -3 }} />
                          <YAxis type="number" dataKey="incidents" name="Incidents" stroke="#64748b" fontSize={9} label={{ value: "Cases", angle: -90, position: "insideLeft" }} />
                          <Tooltip cursor={{ strokeDasharray: "3 3" }} contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Scatter name="Zones" data={filteredData.map((r, i) => ({ heat: r.heat_risk_index, incidents: r.medical_incidents, index: i }))} fill="#f43f5e" />
                        </ScatterChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Ambulance Response dispatch delays across Phase periods
                    </h4>
                    <div className="h-[220px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={PHASES.map((ph) => {
                            const pRows = filteredData.filter((r) => r.phase === ph);
                            const avgLag = pRows.length > 0 
                              ? pRows.reduce((a, b) => a + b.ambulance_response_time, 0) / pRows.length 
                              : 0;
                            return { name: ph.split("-")[0], "Response Delay": parseFloat(avgLag.toFixed(1)) };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Line type="monotone" dataKey="Response Delay" stroke="#06b6d4" strokeWidth={3} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* ── AI Intelligence (at bottom of page, no repeat KPI charts) ── */}
                <AIIntelligence summaryText={contextSummaryText} pageName="Medical & Heat" />
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 4 — SECURITY (Unauthorized intruders, counterfeit ticket cases)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Security" && (
              <div className="space-y-6">
                <PageHeader
                  icon="🔒"
                  title="Stadium Perimeter Security & Incident Tracking Outpost"
                  subtitle="Compiling duplicate ticket passes, perimeter wall breach attempts, ejected spectators and pitch invasions"
                />

                {/* Security KPIs */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <KPICard label="Boundary breach attempts" value={totalUnauthorized.toLocaleString()} type="crit" sub="Unauthorized entries flagged" />
                  <KPICard label="Duplicate Tickets block" value={totalCounterfeit.toLocaleString()} type="warn" sub="Counterfeit passes stopped" />
                  <KPICard label="Intrusion Attempts" value={totalPitchInvasions.toString()} type="crit" sub="General pitch invasions" />
                  <KPICard label="Spectators Ejected" value={totalEjections.toLocaleString()} type="warn" sub="Flagged troublemakers removed" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Left Column: Barricading and breaches */}
                  <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Unauthorized Entry Alarms by Phase Period
                    </h4>
                    <div className="h-[280px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={PHASES.map((ph) => {
                            const pRows = filteredData.filter((r) => r.phase === ph);
                            const totalAttempts = pRows.reduce((a, b) => a + b.unauthorized_entry_attempts, 0);
                            return { name: ph, "Security Alarms": totalAttempts };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Line type="monotone" dataKey="Security Alarms" stroke="#f43f5e" strokeWidth={3} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Total incidents by Arena */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Aggregated Security Incidents by Stadium Venue
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={STADIUMS.map((stad) => ({
                            name: stad.split(" Stadium")[0].split(" ").pop(),
                            "Security Cases": filteredData.filter((r) => r.stadium_name === stad).reduce((a, b) => a + b.security_incidents, 0)
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar fill="#e11d48" dataKey="Security Cases" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* Interactive: Crowd Pressure vs Security Risks scatter */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Spectator Load vs Access Violation Risks
                    </h4>
                    <div className="h-[220px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart>
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis type="number" dataKey="crowd" stroke="#64748b" fontSize={9} label={{ value: "Spectators Count", position: "insideBottom", offset: -3 }} />
                          <YAxis type="number" dataKey="sec" stroke="#64748b" fontSize={9} label={{ value: "Security Alerts", angle: -90, position: "insideLeft" }} />
                          <Tooltip cursor={{ strokeDasharray: "3 3" }} contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Scatter name="Stadium Zones" data={filteredData.map((r, i) => ({ crowd: r.people_count, sec: r.security_incidents + r.unauthorized_entry_attempts, index: i }))} fill="#ef4444" />
                        </ScatterChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      General Security Incidents reported across Phases
                    </h4>
                    <div className="h-[220px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={PHASES.map((ph) => {
                            const pRows = filteredData.filter((r) => r.phase === ph);
                            const totalSec = pRows.reduce((a, b) => a + b.security_incidents, 0);
                            return { name: ph.split("-")[0], "Cases Count": totalSec };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar fill="#b91c1c" dataKey="Cases Count" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* ── AI Intelligence (at bottom of page, no mid-page duplicate components) ── */}
                <AIIntelligence summaryText={contextSummaryText} pageName="Security" />
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 5 — RESOURCE PLANNING (Logistics allocation & staff counts)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Resource Planning" && (
              <div className="space-y-6">
                <PageHeader
                  icon="📦"
                  title="Warden Staffing & crowd Barrier Resource Coordinator"
                  subtitle="Calculating personnel ratios, steel barrier requirements, paramedic medical teams and operational stability ratings"
                />

                {/* Resource KPIs */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <KPICard label="Staff Adequacy Ratio" value={averageStaffRatio.toFixed(2)} type="ok" sub="Staff units per 1K spectators" />
                  <KPICard label="Warden Staff Needed" value={totalRequiredStaff.toLocaleString()} type="info" sub="Total required event personnel" />
                  <KPICard label="Steel Barricades needed" value={totalBarricades.toLocaleString()} type="warn" sub="Crowd control barrier count" />
                  <KPICard label="Medical Squad Teams" value={totalParamedicTeams.toLocaleString()} type="ok" sub="Monitored paramedic squads" />
                </div>

                {/* Resource Action Plan Table */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
                  <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-1.5">
                    Logistic Dispatch Actions Sorted by Highest Priority Threat
                  </h4>
                  <p className="text-[10px] text-slate-500 mb-4">
                    Recommends immediate barricading or warden re-scheduling based on advanced risk weights.
                  </p>

                  <div className="overflow-x-auto border border-slate-800 rounded-xl">
                    <table className="w-full text-left border-collapse text-xs">
                      <thead>
                        <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 font-extrabold uppercase tracking-wider text-[10px]">
                          <th className="p-3">Stadium Venue</th>
                          <th className="p-3">Zone Section</th>
                          <th className="p-3">Zone Type</th>
                          <th className="p-3">Phase Period</th>
                          <th className="p-3 text-center">Risk Score</th>
                          <th className="p-3 text-center">Staff Needed</th>
                          <th className="p-3 text-center">Barricades</th>
                          <th className="p-3">Operations Dispatch Order</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/65 text-slate-300">
                        {filteredData
                          .sort((a, b) => b.risk_score - a.risk_score)
                          .slice(0, 6)
                          .map((row, index) => (
                            <tr key={index} className="hover:bg-slate-950/40">
                              <td className="p-3 font-semibold truncate max-w-[130px]" title={row.stadium_name}>{row.stadium_name.split(" (")[0]}</td>
                              <td className="p-3">{row.zone_name}</td>
                              <td className="p-3">{row.zone_type}</td>
                              <td className="p-3">{row.phase}</td>
                              <td className="p-3 text-center font-mono font-bold text-rose-400">{row.risk_score}</td>
                              <td className="p-3 text-center font-mono font-bold">{row.required_staff}</td>
                              <td className="p-3 text-center font-mono text-slate-400">{row.required_barricades}</td>
                              <td className="p-3 text-xs text-indigo-400 font-medium italic">{row.recommended_action}</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Left Column: Staff adequacy ratio line */}
                  <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Warden Guarding Adequacy ratio trends across Phases
                    </h4>
                    <div className="h-[280px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={PHASES.map((ph) => {
                            const pRows = filteredData.filter((r) => r.phase === ph);
                            const avgRatio = pRows.length > 0 
                              ? pRows.reduce((a, b) => a + b.staff_adequacy_ratio, 0) / pRows.length 
                              : 0;
                            return { name: ph, Ratio: parseFloat(avgRatio.toFixed(2)) };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Line type="monotone" dataKey="Ratio" stroke="#0d9488" strokeWidth={3} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Crowd count vs medical teams scatter */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Paramedic Squad units relative to Crowd Loadings
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart>
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis type="number" dataKey="people" name="Spectators" stroke="#64748b" fontSize={9} />
                          <YAxis type="number" dataKey="med" name="Medical Teams" stroke="#64748b" fontSize={9} />
                          <Tooltip cursor={{ strokeDasharray: "3 3" }} contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Scatter name="Squad Units" data={filteredData.map((r, idx) => ({ people: r.people_count, med: r.deployed_medical_teams, index: idx }))} fill="#0d9488" />
                        </ScatterChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Left Column: Staff vs Medical personnel counts by Zone */}
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Personnel Requirements by Zone Division
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={ZONE_TYPES.map((zt) => {
                            const zRows = filteredData.filter((r) => r.zone_type === zt);
                            const staff = zRows.reduce((a, b) => a + b.required_staff, 0);
                            const med = zRows.reduce((a, b) => a + b.deployed_medical_teams, 0) * 10; // multiplier for visual comparability
                            return { name: zt.split(" ")[0], "Staff Needed": staff, "Medical Squads (x10)": med };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Legend />
                          <Bar dataKey="Staff Needed" fill="#0d9488" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="Medical Squads (x10)" fill="#10b981" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Steel fence assets needed by Zone */}
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Steel Crowd-barricade Deployments by Zone Division
                    </h4>
                    <div className="h-[210px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={ZONE_TYPES.map((zt) => {
                            const zRows = filteredData.filter((r) => r.zone_type === zt);
                            const totalB = zRows.reduce((a, b) => a + b.required_barricades, 0);
                            return { name: zt.split(" ")[0], "Barricades Needed": totalB };
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Bar dataKey="Barricades Needed" fill="#14b8a6" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* ── AI Intelligence (at bottom of page, ensuring no visuals sit below it) ── */}
                <AIIntelligence summaryText={contextSummaryText} pageName="Resource Planning" />
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 6 — RISK MATRIX (Hazard priority listings)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Risk Matrix" && (
              <div className="space-y-6">
                <PageHeader
                  icon="🚨"
                  title="Command Operational Risk Priority Grid & Anomaly Monitor"
                  subtitle="Isolating critical alert status events, threat classifications, and real-time hazard mitigation priorities"
                />

                {/* Matrix KPIs */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <KPICard label="Stadium overall Risk index" value={overallRiskScore.toFixed(2)} type="crit" sub="Combined Weighted Risk Index" />
                  <KPICard label="Critical Alert Records" value={criticalVolume.toString()} type="crit" sub="Spectator density hotspot sectors" />
                  <KPICard label="Alert Watch Records" value={monitorVolume.toString()} type="warn" sub="Moderate threat score points" />
                  <KPICard label="High Bottleneck Counts" value={filteredData.filter((r) => r.avg_queue_wait_time * 2.2 >= 65).length.toString()} type="info" sub="Queue blockings logged" />
                </div>

                {/* Advanced Risk sorted table */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
                    <div>
                      <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest">
                        Full Command Risk Priority List (Ranked Highest Risk First)
                      </h4>
                      <p className="text-[10px] text-slate-500 mt-1">
                        Advanced mathematical tracking of entrance queues, medical lags, security alarms, thermal levels and boundary breaches.
                      </p>
                    </div>
                    {/* Action button */}
                    <button
                      onClick={downloadCSV}
                      className="py-1.5 px-3 bg-violet-600/10 hover:bg-violet-600/20 border border-violet-500/25 rounded-lg text-xs font-bold text-violet-400 flex items-center gap-1.5 cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Export Hazard Manifest (.CSV)</span>
                    </button>
                  </div>

                  <div className="overflow-x-auto border border-slate-800 rounded-xl">
                    <table className="w-full text-left border-collapse text-xs">
                      <thead>
                        <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 font-extrabold uppercase tracking-wider text-[10px]">
                          <th className="p-3">Stadium Venue</th>
                          <th className="p-3">Zone Section</th>
                          <th className="p-3">Zone Division</th>
                          <th className="p-3 text-center">Risk Index</th>
                          <th className="p-3 text-center">Threat Class</th>
                          <th className="p-3">Active Hazard Reason</th>
                          <th className="p-3">Assigned Operations Action</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/65 text-slate-300">
                        {filteredData
                          .sort((a, b) => b.risk_score - a.risk_score)
                          .slice(0, 10)
                          .map((row, i) => (
                            <tr key={i} className="hover:bg-slate-950/40">
                              <td className="p-3 font-semibold truncate max-w-[130px]" title={row.stadium_name}>{row.stadium_name.split(" (")[0]}</td>
                              <td className="p-3 font-mono">{row.zone_name}</td>
                              <td className="p-3">{row.zone_type}</td>
                              <td className="p-3 text-center font-mono font-bold text-violet-400">{row.risk_score}</td>
                              <td className="p-3 text-center">
                                <span className={`px-2 py-0.5 rounded-full text-[9px] font-extrabold leading-none ${row.risk_band === "Critical" ? "bg-rose-500/15 text-rose-400 border border-rose-500/30" : "bg-amber-500/15 text-amber-400 border border-amber-500/30"}`}>
                                  {row.risk_band}
                                </span>
                              </td>
                              <td className="p-3 text-[11px] text-slate-400 font-light">{row.risk_reason}</td>
                              <td className="p-3 text-xs text-emerald-400 font-semibold italic">{row.recommended_action}</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Left Column: Bar chart by Stadium */}
                  <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Average composite operational Risk by Stadium and Zone Type
                    </h4>
                    <div className="h-[280px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={STADIUMS.map((stad) => {
                            const result: any = { name: stad.split(" (")[0].split(" ").pop() };
                            ZONE_TYPES.forEach((zt) => {
                              const sRows = filteredData.filter((r) => r.stadium_name === stad && r.zone_type === zt);
                              const avgRs = sRows.length > 0 
                                ? sRows.reduce((a, b) => a + b.risk_score, 0) / sRows.length 
                                : 0;
                              result[zt.split(" ")[0]] = parseFloat(avgRs.toFixed(1));
                            });
                            return result;
                          })}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                          <YAxis stroke="#64748b" fontSize={10} domain={[0, 100]} />
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                          <Legend />
                          <Bar dataKey="General" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="VIP" fill="#fbbf24" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="Outer" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="Food" fill="#10b981" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Right Column: Risk allocation percentage */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-widest mb-4">
                      Monitored Records Threat density percentages
                    </h4>
                    <div className="h-[200px] w-full flex items-center justify-center">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={[
                              { name: "Severe Threat (68-100)", value: criticalVolume, color: "#e11d48" },
                              { name: "Caution Guard (42-67)", value: monitorVolume, color: "#f59e0b" },
                              { name: "Standard (Under 42)", value: Math.max(0, filteredData.length - criticalVolume - monitorVolume), color: "#0d9488" }
                            ]}
                            cx="50%"
                            cy="50%"
                            innerRadius={50}
                            outerRadius={70}
                            dataKey="value"
                            label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                          >
                            {[
                              { color: "#e11d48" },
                              { color: "#f59e0b" },
                              { color: "#0d9488" }
                            ].map((entry, idx) => (
                              <Cell key={`cell-${idx}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* ── AI Intelligence (at bottom of page, preventing middle page duplicates) ── */}
                <AIIntelligence summaryText={contextSummaryText} pageName="Risk Matrix" />
              </div>
            )}

            {/* ═══════════════════════════════════════════════════════════
                PAGE 7 — ASK AI (Interactive plain language assistant)
                ═══════════════════════════════════════════════════════════ */}
            {activePage === "Ask AI" && (
              <div className="space-y-6">
                <PageHeader
                  icon="💬"
                  title="Operations Command Conversational AI Q&A Assistant"
                  subtitle="Formulate custom operations queries about emergency exits, ambulance lags, warden deployments or stadium anomalies"
                />

                {/* Plain language chat panel */}
                <AskAIPanel contextText={contextSummaryText} />
              </div>
            )}
          </>
        )}

        {/* ── UNIFORM MINIMAL FOOTER ── */}
        <footer className="pt-4 border-t border-slate-900 text-center select-none">
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider flex items-center justify-center gap-1">
            <span>🏏 IPL Crowd Safety Command Platform</span>
            <span className="text-slate-700">•</span>
            <span>Express Full-Stack Architecture</span>
            <span className="text-slate-700">•</span>
            <span>Gemini AI Control Room</span>
          </p>
        </footer>
      </main>
    </div>
  );
}
