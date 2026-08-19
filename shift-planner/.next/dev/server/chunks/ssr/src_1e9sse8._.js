module.exports = [
"[project]/src/app/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>HomePage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$TodayView$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/TodayView.tsx [app-ssr] (ecmascript)");
"use client";
;
;
function HomePage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$TodayView$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["TodayView"], {}, void 0, false, {
        fileName: "[project]/src/app/page.tsx",
        lineNumber: 6,
        columnNumber: 10
    }, this);
}
}),
"[project]/src/components/TodayView.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "TodayView",
    ()=>TodayView
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/rota.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$hooks$2f$useAppData$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/hooks/useAppData.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$pay$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/pay.ts [app-ssr] (ecmascript)");
"use client";
;
;
;
;
;
function countdown(to, now) {
    const ms = Math.max(0, to.getTime() - now.getTime());
    const totalMins = Math.floor(ms / 60000);
    const d = Math.floor(totalMins / (60 * 24));
    const h = Math.floor(totalMins % (60 * 24) / 60);
    const m = totalMins % 60;
    if (d > 0) return `${d}d ${h}h ${m}m`;
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
}
function dateKeyFrom(d) {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
function findNextStart(today, upcoming, now) {
    const candidates = [
        today,
        ...upcoming
    ].filter((s)=>s.kind !== "off");
    for (const target of candidates){
        const start = new Date(target.date);
        start.setHours(target.startHour ?? 0, 0, 0, 0);
        if (start.getTime() > now.getTime()) return {
            shift: target,
            at: start
        };
        if ((0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["isSameDay"])(target.date, now)) {
            const end = target.kind === "day" ? new Date(target.date.getFullYear(), target.date.getMonth(), target.date.getDate(), 18) : new Date(target.date.getFullYear(), target.date.getMonth(), target.date.getDate() + 1, 6);
            if (now.getTime() < end.getTime()) return {
                shift: target,
                at: start
            };
        }
    }
    return null;
}
function TodayView() {
    const { data, setDayNote, addOvertime } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$hooks$2f$useAppData$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useAppData"])();
    const [now, setNow] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(()=>new Date());
    const [otHours, setOtHours] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("2");
    const [otNote, setOtNote] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("");
    const [noteDraft, setNoteDraft] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const t = window.setInterval(()=>setNow(new Date()), 30_000);
        return ()=>window.clearInterval(t);
    }, []);
    const today = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getShiftForDate"])(now);
    const key = dateKeyFrom(now);
    const savedNote = data.notes.find((n)=>n.dateKey === key)?.text ?? "";
    const note = noteDraft ?? savedNote;
    const upcoming = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getUpcomingShifts"])(now, 6);
    const monthPay = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$pay$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["calculateMonthPay"])(data, now.getFullYear(), now.getMonth());
    const wakeTarget = today.kind !== "off" ? today : upcoming[0];
    const wake = wakeTarget ? (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getWakeTime"])(wakeTarget.date, wakeTarget.kind === "day" ? data.settings.dayWakeLeadMinutes : data.settings.nightWakeLeadMinutes) : null;
    const nextStart = findNextStart(today, upcoming, now);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "stack",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                className: `hero-shift kind-${today.kind}`,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "hero-date",
                        children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["formatLongDate"])(now)
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 89,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                        className: "hero-title",
                        children: today.label
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 90,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "hero-time",
                        children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["formatShiftTime"])(today)
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 91,
                        columnNumber: 9
                    }, this),
                    nextStart && nextStart.at.getTime() > now.getTime() && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "hero-count",
                        children: [
                            "Starts in ",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: countdown(nextStart.at, now)
                            }, void 0, false, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 94,
                                columnNumber: 23
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 93,
                        columnNumber: 11
                    }, this),
                    nextStart && nextStart.at.getTime() <= now.getTime() && today.kind !== "off" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "hero-count",
                        children: "On shift now"
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 98,
                        columnNumber: 11
                    }, this),
                    wake && wake.getTime() > now.getTime() && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "hero-wake",
                        children: [
                            "Wake alarm ·",
                            " ",
                            wake.toLocaleTimeString(undefined, {
                                hour: "2-digit",
                                minute: "2-digit"
                            })
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 101,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/TodayView.tsx",
                lineNumber: 88,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                className: "panel stats-row",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "stat-label",
                                children: "This month"
                            }, void 0, false, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 110,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "stat-value",
                                children: [
                                    monthPay.scheduledDays + monthPay.scheduledNights,
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: " days"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/TodayView.tsx",
                                        lineNumber: 113,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 111,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 109,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "stat-label",
                                children: "Hours"
                            }, void 0, false, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 117,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "stat-value",
                                children: [
                                    monthPay.scheduledHours,
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        children: "h"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/TodayView.tsx",
                                        lineNumber: 120,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 118,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 116,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "stat-label",
                                children: "Est. pay"
                            }, void 0, false, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 124,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "stat-value money",
                                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$pay$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["money"])(monthPay.total, data.settings.currency)
                            }, void 0, false, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 125,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 123,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/TodayView.tsx",
                lineNumber: 108,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                className: "panel",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "panel-head",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            children: "Coming up"
                        }, void 0, false, {
                            fileName: "[project]/src/components/TodayView.tsx",
                            lineNumber: 131,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 130,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                        className: "shift-list",
                        children: upcoming.map((s)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                className: `shift-row kind-${s.kind}`,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "shift-label",
                                                children: s.label
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/TodayView.tsx",
                                                lineNumber: 137,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                className: "shift-meta",
                                                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["formatShortDate"])(s.date)
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/TodayView.tsx",
                                                lineNumber: 138,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/TodayView.tsx",
                                        lineNumber: 136,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                        className: "shift-hours",
                                        children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["formatShiftTime"])(s)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/TodayView.tsx",
                                        lineNumber: 140,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, s.date.toISOString(), true, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 135,
                                columnNumber: 13
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 133,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/TodayView.tsx",
                lineNumber: 129,
                columnNumber: 7
            }, this),
            today.kind !== "off" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                className: "panel",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "panel-head",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            children: "Log overtime"
                        }, void 0, false, {
                            fileName: "[project]/src/components/TodayView.tsx",
                            lineNumber: 149,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 148,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "form-row",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                children: [
                                    "Hours",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                        type: "number",
                                        min: "0.25",
                                        step: "0.25",
                                        value: otHours,
                                        onChange: (e)=>setOtHours(e.target.value)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/TodayView.tsx",
                                        lineNumber: 154,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 152,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                className: "grow",
                                children: [
                                    "Note",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                        type: "text",
                                        placeholder: "Cover / handover / call-in",
                                        value: otNote,
                                        onChange: (e)=>setOtNote(e.target.value)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/TodayView.tsx",
                                        lineNumber: 164,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/TodayView.tsx",
                                lineNumber: 162,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 151,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        type: "button",
                        className: "btn btn-primary",
                        onClick: ()=>{
                            const hours = Number(otHours);
                            if (!hours || hours <= 0) return;
                            addOvertime({
                                dateKey: key,
                                hours,
                                note: otNote
                            });
                            setOtNote("");
                        },
                        children: "Add overtime"
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 172,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/TodayView.tsx",
                lineNumber: 147,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
                className: "panel",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "panel-head",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            children: "Today's note"
                        }, void 0, false, {
                            fileName: "[project]/src/components/TodayView.tsx",
                            lineNumber: 193,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 192,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                        rows: 3,
                        placeholder: "Handover, parking, PPE reminder…",
                        value: note,
                        onChange: (e)=>setNoteDraft(e.target.value),
                        onBlur: ()=>{
                            setDayNote(now, note);
                            setNoteDraft(null);
                        }
                    }, void 0, false, {
                        fileName: "[project]/src/components/TodayView.tsx",
                        lineNumber: 195,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/TodayView.tsx",
                lineNumber: 191,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/TodayView.tsx",
        lineNumber: 87,
        columnNumber: 5
    }, this);
}
}),
"[project]/src/lib/pay.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "calculateMonthPay",
    ()=>calculateMonthPay,
    "calculatePay",
    ()=>calculatePay,
    "estimatedAnnual",
    ()=>estimatedAnnual,
    "money",
    ()=>money,
    "monthRange",
    ()=>monthRange,
    "parseMonthKey",
    ()=>parseMonthKey,
    "sumAdjustments",
    ()=>sumAdjustments,
    "sumOvertimeHours",
    ()=>sumOvertimeHours,
    "workedDaysInMonth",
    ()=>workedDaysInMonth,
    "yearToDatePay",
    ()=>yearToDatePay
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/rota.ts [app-ssr] (ecmascript)");
;
function money(amount, currency) {
    try {
        return new Intl.NumberFormat(undefined, {
            style: "currency",
            currency,
            maximumFractionDigits: 2
        }).format(amount);
    } catch  {
        return `${currency} ${amount.toFixed(2)}`;
    }
}
function monthRange(year, month) {
    return {
        start: new Date(year, month, 1),
        end: new Date(year, month + 1, 0)
    };
}
function calculatePay(data, start, end) {
    const { settings } = data;
    const counts = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["countWorkDaysInRange"])(start, end);
    const basePay = counts.hours * settings.hourlyRate;
    const nightPremiumPay = counts.nights * 12 * settings.nightPremium;
    const startKey = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(start));
    const endKey = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(end));
    const ot = data.overtime.filter((o)=>o.dateKey >= startKey && o.dateKey <= endKey);
    const overtimeHours = ot.reduce((sum, o)=>sum + o.hours, 0);
    const overtimePay = ot.reduce((sum, o)=>{
        const rate = o.rateOverride ?? settings.hourlyRate * settings.overtimeMultiplier;
        return sum + o.hours * rate;
    }, 0);
    const adjustmentsList = data.adjustments.filter((a)=>a.dateKey >= startKey && a.dateKey <= endKey);
    const adjustments = adjustmentsList.reduce((sum, a)=>sum + a.amount, 0);
    const total = basePay + nightPremiumPay + overtimePay + adjustments;
    const effectiveHourly = counts.hours + overtimeHours > 0 ? total / (counts.hours + overtimeHours) : 0;
    return {
        scheduledDays: counts.days,
        scheduledNights: counts.nights,
        scheduledHours: counts.hours,
        basePay,
        nightPremiumPay,
        overtimeHours,
        overtimePay,
        adjustments,
        total,
        effectiveHourly
    };
}
function calculateMonthPay(data, year, month) {
    const { start, end } = monthRange(year, month);
    return calculatePay(data, start, end);
}
function workedDaysInMonth(data, year, month) {
    const { start, end } = monthRange(year, month);
    const rows = [];
    const cursor = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(start);
    const last = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(end);
    while(cursor.getTime() <= last.getTime()){
        const shift = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getShiftForDate"])(cursor);
        if (shift.kind !== "off") {
            const key = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])(cursor);
            const ot = data.overtime.filter((o)=>o.dateKey === key).reduce((s, o)=>s + o.hours, 0);
            const note = data.notes.find((n)=>n.dateKey === key)?.text ?? "";
            rows.push({
                dateKey: key,
                kind: shift.kind,
                scheduledHours: shift.hours,
                overtimeHours: ot,
                note
            });
        }
        cursor.setDate(cursor.getDate() + 1);
    }
    return rows;
}
function sumOvertimeHours(entries) {
    return entries.reduce((s, e)=>s + e.hours, 0);
}
function sumAdjustments(entries) {
    return entries.reduce((s, e)=>s + e.amount, 0);
}
function yearToDatePay(data, asOf = new Date()) {
    const start = new Date(asOf.getFullYear(), 0, 1);
    return calculatePay(data, start, asOf);
}
function estimatedAnnual(data) {
    // Rough: 4 work days per 7-day cycle on 2-2-3
    const workDaysPerYear = 4 / 7 * 365.25;
    const hours = workDaysPerYear * 12;
    const base = hours * data.settings.hourlyRate;
    const nightsShare = 0.5;
    const nightPrem = workDaysPerYear * nightsShare * 12 * data.settings.nightPremium;
    return base + nightPrem;
}
function parseMonthKey(dateKey) {
    const d = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["parseDateKey"])(dateKey);
    return {
        year: d.getFullYear(),
        month: d.getMonth()
    };
}
}),
];

//# sourceMappingURL=src_1e9sse8._.js.map