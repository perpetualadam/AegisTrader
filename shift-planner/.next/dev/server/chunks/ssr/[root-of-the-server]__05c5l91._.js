module.exports = [
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/action-async-storage.external.js [external] (next/dist/server/app-render/action-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/action-async-storage.external.js", () => require("next/dist/server/app-render/action-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/after-task-async-storage.external.js [external] (next/dist/server/app-render/after-task-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/after-task-async-storage.external.js", () => require("next/dist/server/app-render/after-task-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/dynamic-access-async-storage.external.js [external] (next/dist/server/app-render/dynamic-access-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/dynamic-access-async-storage.external.js", () => require("next/dist/server/app-render/dynamic-access-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/runtime-reacts.external.js [external] (next/dist/server/runtime-reacts.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/server/runtime-reacts.external.js", () => require("next/dist/server/runtime-reacts.external.js"));

module.exports = mod;
}),
"[project]/src/components/AppShell.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AppShell",
    ()=>AppShell
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$hooks$2f$useAppData$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/hooks/useAppData.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$notifications$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/notifications.ts [app-ssr] (ecmascript)");
"use client";
;
;
;
;
;
;
const NAV = [
    {
        href: "/",
        label: "Today",
        icon: "◉"
    },
    {
        href: "/calendar",
        label: "Rota",
        icon: "▦"
    },
    {
        href: "/pay",
        label: "Pay",
        icon: "£"
    },
    {
        href: "/alarms",
        label: "Alarms",
        icon: "◎"
    },
    {
        href: "/settings",
        label: "More",
        icon: "☰"
    }
];
function subscribeOnline(cb) {
    window.addEventListener("online", cb);
    window.addEventListener("offline", cb);
    return ()=>{
        window.removeEventListener("online", cb);
        window.removeEventListener("offline", cb);
    };
}
function getOnlineSnapshot() {
    return navigator.onLine;
}
function getOnlineServerSnapshot() {
    return true;
}
function AppShell({ children }) {
    const pathname = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["usePathname"])();
    const { data, setData } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$hooks$2f$useAppData$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useAppData"])();
    const online = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useSyncExternalStore"])(subscribeOnline, getOnlineSnapshot, getOnlineServerSnapshot);
    const [alarm, setAlarm] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [installPrompt, setInstallPrompt] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const stop = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$notifications$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startNotificationWatchdog"])(()=>data.settings);
        return stop;
    }, [
        data.settings
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const onRing = (e)=>{
            const detail = e.detail;
            setAlarm(detail);
        };
        const onDismiss = ()=>setAlarm(null);
        window.addEventListener("shift-alarm-ring", onRing);
        window.addEventListener("shift-alarm-dismiss", onDismiss);
        return ()=>{
            window.removeEventListener("shift-alarm-ring", onRing);
            window.removeEventListener("shift-alarm-dismiss", onDismiss);
        };
    }, []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handler = (e)=>{
            e.preventDefault();
            setInstallPrompt(e);
        };
        window.addEventListener("beforeinstallprompt", handler);
        return ()=>window.removeEventListener("beforeinstallprompt", handler);
    }, []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if ("serviceWorker" in navigator) {
            void navigator.serviceWorker.register("/sw.js").catch(()=>undefined);
        }
    }, []);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "app-root",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "app-glow",
                "aria-hidden": true
            }, void 0, false, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 82,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
                className: "topbar",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "brand",
                                children: data.settings.plantName
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 85,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                className: "brand-sub",
                                children: [
                                    data.settings.shiftName,
                                    " · 2-2-3"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 86,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 84,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "topbar-right",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: `pill ${online ? "online" : "offline"}`,
                            children: online ? "Online" : "Offline"
                        }, void 0, false, {
                            fileName: "[project]/src/components/AppShell.tsx",
                            lineNumber: 89,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 88,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 83,
                columnNumber: 7
            }, this),
            !data.notificationPermissionAsked && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "banner",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: "Enable reminders"
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 98,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: "Day-before alerts at 5pm & 8pm, plus wake alarms."
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 99,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 97,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        type: "button",
                        className: "btn btn-primary",
                        onClick: async ()=>{
                            await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$notifications$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ensureNotificationPermission"])();
                            setData({
                                ...data,
                                notificationPermissionAsked: true
                            });
                        },
                        children: "Allow"
                    }, void 0, false, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 101,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        type: "button",
                        className: "btn btn-ghost",
                        onClick: ()=>setData({
                                ...data,
                                notificationPermissionAsked: true
                            }),
                        children: "Later"
                    }, void 0, false, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 111,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 96,
                columnNumber: 9
            }, this),
            installPrompt && !data.installedHintDismissed && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "banner install",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                children: "Install on your phone"
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 124,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                children: "Add to home screen for offline use & faster alarms."
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 125,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 123,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        type: "button",
                        className: "btn btn-primary",
                        onClick: async ()=>{
                            await installPrompt.prompt();
                            setInstallPrompt(null);
                            setData({
                                ...data,
                                installedHintDismissed: true
                            });
                        },
                        children: "Install"
                    }, void 0, false, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 127,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        type: "button",
                        className: "btn btn-ghost",
                        onClick: ()=>{
                            setInstallPrompt(null);
                            setData({
                                ...data,
                                installedHintDismissed: true
                            });
                        },
                        children: "Dismiss"
                    }, void 0, false, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 138,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 122,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
                className: "main",
                children: children
            }, void 0, false, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 151,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("nav", {
                className: "bottom-nav",
                "aria-label": "Primary",
                children: NAV.map((item)=>{
                    const active = pathname === item.href;
                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                        href: item.href,
                        className: `nav-item ${active ? "active" : ""}`,
                        "aria-current": active ? "page" : undefined,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "nav-icon",
                                "aria-hidden": true,
                                children: item.icon
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 163,
                                columnNumber: 15
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: item.label
                            }, void 0, false, {
                                fileName: "[project]/src/components/AppShell.tsx",
                                lineNumber: 166,
                                columnNumber: 15
                            }, this)
                        ]
                    }, item.href, true, {
                        fileName: "[project]/src/components/AppShell.tsx",
                        lineNumber: 157,
                        columnNumber: 13
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 153,
                columnNumber: 7
            }, this),
            alarm && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "alarm-overlay",
                role: "alertdialog",
                "aria-modal": "true",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "alarm-card",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            className: "alarm-kicker",
                            children: "Wake alarm"
                        }, void 0, false, {
                            fileName: "[project]/src/components/AppShell.tsx",
                            lineNumber: 175,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                            children: alarm.title
                        }, void 0, false, {
                            fileName: "[project]/src/components/AppShell.tsx",
                            lineNumber: 176,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                            children: alarm.body
                        }, void 0, false, {
                            fileName: "[project]/src/components/AppShell.tsx",
                            lineNumber: 177,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            type: "button",
                            className: "btn btn-primary btn-lg",
                            onClick: ()=>{
                                (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$notifications$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["dismissAlarm"])();
                                setAlarm(null);
                            },
                            children: "Dismiss"
                        }, void 0, false, {
                            fileName: "[project]/src/components/AppShell.tsx",
                            lineNumber: 178,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/AppShell.tsx",
                    lineNumber: 174,
                    columnNumber: 11
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/AppShell.tsx",
                lineNumber: 173,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/AppShell.tsx",
        lineNumber: 81,
        columnNumber: 5
    }, this);
}
}),
"[project]/src/hooks/useAppData.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useAppData",
    ()=>useAppData
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/storage.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/rota.ts [app-ssr] (ecmascript)");
"use client";
;
;
;
function subscribe(cb) {
    const onChange = ()=>cb();
    window.addEventListener("shift-data-changed", onChange);
    window.addEventListener("storage", onChange);
    return ()=>{
        window.removeEventListener("shift-data-changed", onChange);
        window.removeEventListener("storage", onChange);
    };
}
function getSnapshot() {
    return localStorage.getItem("plastics-b-shift-planner-v1") ?? "";
}
function getServerSnapshot() {
    return "";
}
function useAppData() {
    const raw = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useSyncExternalStore"])(subscribe, getSnapshot, getServerSnapshot);
    const data = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useMemo"])(()=>{
        if (!raw) {
            // Ensure defaults even when key missing
            return (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loadData"])();
        }
        try {
            return (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loadData"])();
        } catch  {
            return (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loadData"])();
        }
    }, [
        raw
    ]);
    const setData = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((updater)=>{
        const prev = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loadData"])();
        const next = typeof updater === "function" ? updater(prev) : updater;
        (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["saveData"])(next);
    }, []);
    const updateSettings = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((partial)=>{
        setData((prev)=>({
                ...prev,
                settings: {
                    ...prev.settings,
                    ...partial
                }
            }));
    }, [
        setData
    ]);
    const addOvertime = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((entry)=>{
        setData((prev)=>({
                ...prev,
                overtime: [
                    ...prev.overtime,
                    {
                        ...entry,
                        id: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["uid"])(),
                        createdAt: new Date().toISOString()
                    }
                ]
            }));
    }, [
        setData
    ]);
    const removeOvertime = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((id)=>{
        setData((prev)=>({
                ...prev,
                overtime: prev.overtime.filter((o)=>o.id !== id)
            }));
    }, [
        setData
    ]);
    const setDayNote = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((date, text)=>{
        const key = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])(date);
        setData((prev)=>{
            const notes = prev.notes.filter((n)=>n.dateKey !== key);
            if (text.trim()) notes.push({
                dateKey: key,
                text: text.trim()
            });
            return {
                ...prev,
                notes
            };
        });
    }, [
        setData
    ]);
    const addAdjustment = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((label, amount, dateKey)=>{
        setData((prev)=>({
                ...prev,
                adjustments: [
                    ...prev.adjustments,
                    {
                        id: (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$storage$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["uid"])(),
                        label,
                        amount,
                        dateKey
                    }
                ]
            }));
    }, [
        setData
    ]);
    const removeAdjustment = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((id)=>{
        setData((prev)=>({
                ...prev,
                adjustments: prev.adjustments.filter((a)=>a.id !== id)
            }));
    }, [
        setData
    ]);
    return {
        data,
        setData,
        updateSettings,
        addOvertime,
        removeOvertime,
        setDayNote,
        addAdjustment,
        removeAdjustment
    };
}
}),
"[project]/src/lib/notifications.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "buildSchedule",
    ()=>buildSchedule,
    "canNotify",
    ()=>canNotify,
    "dismissAlarm",
    ()=>dismissAlarm,
    "ensureNotificationPermission",
    ()=>ensureNotificationPermission,
    "fireEvent",
    ()=>fireEvent,
    "isAlarmRinging",
    ()=>isAlarmRinging,
    "nextEventSummary",
    ()=>nextEventSummary,
    "showNotification",
    ()=>showNotification,
    "startNotificationWatchdog",
    ()=>startNotificationWatchdog,
    "todayStatus",
    ()=>todayStatus,
    "tomorrowShiftPreview",
    ()=>tomorrowShiftPreview
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/rota.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$sounds$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/sounds.ts [app-ssr] (ecmascript)");
;
;
const FIRED_KEY = "plastics-b-shift-fired-v1";
function loadFired() {
    try {
        return JSON.parse(localStorage.getItem(FIRED_KEY) ?? "{}");
    } catch  {
        return {};
    }
}
function markFired(id) {
    const map = loadFired();
    map[id] = Date.now();
    // prune older than 14 days
    const cutoff = Date.now() - 14 * 24 * 60 * 60 * 1000;
    for (const [k, v] of Object.entries(map)){
        if (v < cutoff) delete map[k];
    }
    localStorage.setItem(FIRED_KEY, JSON.stringify(map));
}
function wasFired(id) {
    return Boolean(loadFired()[id]);
}
async function ensureNotificationPermission() {
    if ("TURBOPACK compile-time truthy", 1) return "denied";
    //TURBOPACK unreachable
    ;
}
function canNotify() {
    return ("TURBOPACK compile-time value", "undefined") !== "undefined" && "Notification" in window && Notification.permission === "granted";
}
function showNotification(title, body, tag) {
    if (!canNotify()) return;
    //TURBOPACK unreachable
    ;
}
function parseTimeOnDate(day, hhmm) {
    const [h, m] = hhmm.split(":").map(Number);
    const d = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(day);
    d.setHours(h, m, 0, 0);
    return d;
}
function buildSchedule(settings, from = new Date()) {
    const events = [];
    const today = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(from);
    if (settings.remindersEnabled) {
        const reminderDays = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getReminderDates"])(today, 45);
        for (const day of reminderDays){
            const tomorrow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["addDays"])(day, 1);
            const shift = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getShiftForDate"])(tomorrow);
            for (const time of settings.reminderTimes){
                const at = parseTimeOnDate(day, time);
                if (at.getTime() < from.getTime() - 60_000) continue;
                events.push({
                    id: `reminder-${(0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])(day)}-${time}`,
                    at,
                    type: "reminder",
                    title: `${settings.shiftName} tomorrow`,
                    body: `${shift.label} ${(0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["formatShiftTime"])(shift)} — get ready.`
                });
            }
        }
    }
    if (settings.wakeAlarmsEnabled) {
        for(let i = 0; i < 30; i++){
            const day = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["addDays"])(today, i);
            const shift = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getShiftForDate"])(day);
            if (shift.kind === "off") continue;
            const lead = shift.kind === "day" ? settings.dayWakeLeadMinutes : settings.nightWakeLeadMinutes;
            const at = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getWakeTime"])(day, lead);
            if (!at || at.getTime() < from.getTime() - 60_000) continue;
            events.push({
                id: `wake-${(0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])(day)}`,
                at,
                type: "wake",
                title: `Wake up — ${shift.label}`,
                body: `${settings.plantName} ${settings.shiftName}: ${(0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["formatShiftTime"])(shift)} starts soon.`
            });
        }
    }
    return events.sort((a, b)=>a.at.getTime() - b.at.getTime());
}
let watchdog = null;
let ringing = false;
function isAlarmRinging() {
    return ringing;
}
async function fireEvent(event, settings) {
    if (wasFired(event.id)) return;
    markFired(event.id);
    showNotification(event.title, event.body, event.id);
    if (event.type === "wake") {
        ringing = true;
        window.dispatchEvent(new CustomEvent("shift-alarm-ring", {
            detail: event
        }));
        try {
            // Loop sound for ~45s while ringing
            const until = Date.now() + 45_000;
            while(ringing && Date.now() < until){
                await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$sounds$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["playAlarmSound"])(settings.alarmSound, settings.alarmVolume, 1);
            }
        } finally{
            ringing = false;
        }
    }
}
function dismissAlarm() {
    ringing = false;
    window.dispatchEvent(new CustomEvent("shift-alarm-dismiss"));
}
function startNotificationWatchdog(getSettings) {
    if (watchdog) window.clearInterval(watchdog);
    const tick = ()=>{
        const settings = getSettings();
        const now = new Date();
        const events = buildSchedule(settings, new Date(now.getTime() - 30_000));
        for (const event of events){
            const delta = event.at.getTime() - now.getTime();
            if (delta <= 0 && delta > -90_000 && !wasFired(event.id)) {
                void fireEvent(event, settings);
            }
        }
        // Persist next few for service worker
        const upcoming = events.filter((e)=>e.at.getTime() >= now.getTime()).slice(0, 20);
        try {
            localStorage.setItem("plastics-b-shift-schedule", JSON.stringify(upcoming.map((e)=>({
                    id: e.id,
                    at: e.at.toISOString(),
                    type: e.type,
                    title: e.title,
                    body: e.body
                }))));
        } catch  {
        // ignore
        }
        if (navigator.serviceWorker?.controller) {
            navigator.serviceWorker.controller.postMessage({
                type: "SYNC_SCHEDULE",
                events: upcoming.map((e)=>({
                        id: e.id,
                        at: e.at.toISOString(),
                        type: e.type,
                        title: e.title,
                        body: e.body
                    }))
            });
        }
    };
    tick();
    watchdog = window.setInterval(tick, 20_000);
    return ()=>{
        if (watchdog) window.clearInterval(watchdog);
        watchdog = null;
    };
}
function nextEventSummary(settings) {
    const events = buildSchedule(settings, new Date());
    return events[0] ?? null;
}
function tomorrowShiftPreview(from = new Date()) {
    const tomorrow = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["addDays"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["startOfLocalDay"])(from), 1);
    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getShiftForDate"])(tomorrow);
}
function todayStatus(from = new Date()) {
    const today = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getShiftForDate"])(from);
    const next = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getNextWorkingShift"])(from);
    return {
        today,
        next
    };
}
}),
"[project]/src/lib/rota.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/** Plastics B-Shift rota — 2 days / 2 nights / 3 off (7-day cycle) */ __turbopack_context__.s([
    "CYCLE_ANCHOR",
    ()=>CYCLE_ANCHOR,
    "CYCLE_LENGTH",
    ()=>CYCLE_LENGTH,
    "DAY_SHIFT_HOURS",
    ()=>DAY_SHIFT_HOURS,
    "NIGHT_SHIFT_HOURS",
    ()=>NIGHT_SHIFT_HOURS,
    "SHIFT_NAME",
    ()=>SHIFT_NAME,
    "addDays",
    ()=>addDays,
    "countWorkDaysInRange",
    ()=>countWorkDaysInRange,
    "cycleLegend",
    ()=>cycleLegend,
    "formatLongDate",
    ()=>formatLongDate,
    "formatShiftTime",
    ()=>formatShiftTime,
    "formatShortDate",
    ()=>formatShortDate,
    "getCycleDay",
    ()=>getCycleDay,
    "getMonthShifts",
    ()=>getMonthShifts,
    "getNextWorkingShift",
    ()=>getNextWorkingShift,
    "getReminderDates",
    ()=>getReminderDates,
    "getShiftEnd",
    ()=>getShiftEnd,
    "getShiftForDate",
    ()=>getShiftForDate,
    "getShiftStart",
    ()=>getShiftStart,
    "getUpcomingShifts",
    ()=>getUpcomingShifts,
    "getWakeTime",
    ()=>getWakeTime,
    "isSameDay",
    ()=>isSameDay,
    "parseDateKey",
    ()=>parseDateKey,
    "startOfLocalDay",
    ()=>startOfLocalDay,
    "toDateKey",
    ()=>toDateKey
]);
const CYCLE_ANCHOR = new Date(2026, 0, 3);
const CYCLE_LENGTH = 7;
const DAY_SHIFT_HOURS = 12;
const NIGHT_SHIFT_HOURS = 12;
const SHIFT_NAME = "B Shift";
const CYCLE_PATTERN = [
    "day",
    "day",
    "night",
    "night",
    "off",
    "off",
    "off"
];
function startOfLocalDay(d) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}
function diffDays(a, b) {
    const ms = startOfLocalDay(a).getTime() - startOfLocalDay(b).getTime();
    return Math.round(ms / (1000 * 60 * 60 * 24));
}
function toDateKey(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
}
function parseDateKey(key) {
    const [y, m, d] = key.split("-").map(Number);
    return new Date(y, m - 1, d);
}
function getCycleDay(date) {
    const delta = diffDays(date, CYCLE_ANCHOR);
    return (delta % CYCLE_LENGTH + CYCLE_LENGTH) % CYCLE_LENGTH;
}
function getShiftForDate(date) {
    const cycleDay = getCycleDay(date);
    const kind = CYCLE_PATTERN[cycleDay];
    const day = startOfLocalDay(date);
    if (kind === "day") {
        return {
            date: day,
            kind,
            cycleDay,
            label: "Day shift",
            startHour: 6,
            endHour: 18,
            hours: DAY_SHIFT_HOURS
        };
    }
    if (kind === "night") {
        return {
            date: day,
            kind,
            cycleDay,
            label: "Night shift",
            startHour: 18,
            endHour: 6,
            hours: NIGHT_SHIFT_HOURS
        };
    }
    return {
        date: day,
        kind: "off",
        cycleDay,
        label: "Off",
        startHour: null,
        endHour: null,
        hours: 0
    };
}
function formatShiftTime(shift) {
    if (shift.kind === "day") return "06:00 – 18:00";
    if (shift.kind === "night") return "18:00 – 06:00";
    return "Rest day";
}
function getShiftStart(date) {
    const shift = getShiftForDate(date);
    if (shift.kind === "off" || shift.startHour === null) return null;
    const start = startOfLocalDay(date);
    start.setHours(shift.startHour, 0, 0, 0);
    return start;
}
function getShiftEnd(date) {
    const shift = getShiftForDate(date);
    if (shift.kind === "off") return null;
    const day = startOfLocalDay(date);
    if (shift.kind === "day") {
        return new Date(day.getFullYear(), day.getMonth(), day.getDate(), 18, 0, 0, 0);
    }
    return new Date(day.getFullYear(), day.getMonth(), day.getDate() + 1, 6, 0, 0, 0);
}
function getWakeTime(date, leadMinutes) {
    const start = getShiftStart(date);
    if (!start) return null;
    return new Date(start.getTime() - leadMinutes * 60 * 1000);
}
function getMonthShifts(year, month) {
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const out = [];
    for(let d = 1; d <= daysInMonth; d++){
        out.push(getShiftForDate(new Date(year, month, d)));
    }
    return out;
}
function getUpcomingShifts(from, count) {
    const out = [];
    let cursor = startOfLocalDay(from);
    let guard = 0;
    while(out.length < count && guard < 400){
        const shift = getShiftForDate(cursor);
        if (shift.kind !== "off") out.push(shift);
        cursor = new Date(cursor.getFullYear(), cursor.getMonth(), cursor.getDate() + 1);
        guard++;
    }
    return out;
}
function getNextWorkingShift(from = new Date()) {
    const now = from;
    let cursor = startOfLocalDay(now);
    for(let i = 0; i < 20; i++){
        const shift = getShiftForDate(cursor);
        if (shift.kind !== "off") {
            const start = getShiftStart(cursor);
            const end = getShiftEnd(cursor);
            if (start && start.getTime() > now.getTime()) return shift;
            if (i === 0 && start && end && now.getTime() < end.getTime()) return shift;
        }
        cursor = new Date(cursor.getFullYear(), cursor.getMonth(), cursor.getDate() + 1);
    }
    return null;
}
function isSameDay(a, b) {
    return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}
function countWorkDaysInRange(start, end) {
    let days = 0;
    let nights = 0;
    let off = 0;
    let hours = 0;
    const cursor = startOfLocalDay(start);
    const last = startOfLocalDay(end);
    while(cursor.getTime() <= last.getTime()){
        const s = getShiftForDate(cursor);
        if (s.kind === "day") {
            days++;
            hours += s.hours;
        } else if (s.kind === "night") {
            nights++;
            hours += s.hours;
        } else {
            off++;
        }
        cursor.setDate(cursor.getDate() + 1);
    }
    return {
        days,
        nights,
        off,
        hours
    };
}
function cycleLegend() {
    return [
        {
            kind: "day",
            days: 2,
            label: "2 day shifts"
        },
        {
            kind: "night",
            days: 2,
            label: "2 night shifts"
        },
        {
            kind: "off",
            days: 3,
            label: "3 days off"
        }
    ];
}
function formatShortDate(d) {
    return d.toLocaleDateString(undefined, {
        weekday: "short",
        day: "numeric",
        month: "short"
    });
}
function formatLongDate(d) {
    return d.toLocaleDateString(undefined, {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });
}
function addDays(d, n) {
    const out = startOfLocalDay(d);
    out.setDate(out.getDate() + n);
    return out;
}
function getReminderDates(from, aheadDays = 60) {
    const dates = [];
    let cursor = startOfLocalDay(from);
    for(let i = 0; i < aheadDays; i++){
        const tomorrow = addDays(cursor, 1);
        const shift = getShiftForDate(tomorrow);
        if (shift.kind !== "off") dates.push(new Date(cursor));
        cursor = addDays(cursor, 1);
    }
    return dates;
}
}),
"[project]/src/lib/sounds.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "SOUND_OPTIONS",
    ()=>SOUND_OPTIONS,
    "playAlarmSound",
    ()=>playAlarmSound,
    "stopAlarmAudio",
    ()=>stopAlarmAudio
]);
const SOUND_OPTIONS = [
    {
        id: "pulse",
        label: "Pulse",
        description: "Steady dual-tone wake"
    },
    {
        id: "radar",
        label: "Radar",
        description: "Rising sweep"
    },
    {
        id: "chime",
        label: "Chime",
        description: "Clear bell tones"
    },
    {
        id: "buzzer",
        label: "Buzzer",
        description: "Hard industrial buzz"
    },
    {
        id: "gentle",
        label: "Gentle",
        description: "Soft ascending pad"
    },
    {
        id: "siren",
        label: "Siren",
        description: "Urgent alternating tones"
    }
];
const PATTERNS = {
    pulse: [
        {
            freq: 880,
            dur: 0.18,
            type: "square"
        },
        {
            freq: 660,
            dur: 0.18,
            type: "square",
            gap: 0.08
        },
        {
            freq: 880,
            dur: 0.18,
            type: "square",
            gap: 0.08
        },
        {
            freq: 660,
            dur: 0.28,
            type: "square",
            gap: 0.08
        }
    ],
    radar: [
        {
            freq: 420,
            dur: 0.35,
            type: "sawtooth"
        },
        {
            freq: 640,
            dur: 0.35,
            type: "sawtooth",
            gap: 0.05
        },
        {
            freq: 880,
            dur: 0.45,
            type: "sawtooth",
            gap: 0.05
        }
    ],
    chime: [
        {
            freq: 523.25,
            dur: 0.4,
            type: "sine"
        },
        {
            freq: 659.25,
            dur: 0.4,
            type: "sine",
            gap: 0.1
        },
        {
            freq: 783.99,
            dur: 0.55,
            type: "sine",
            gap: 0.1
        }
    ],
    buzzer: [
        {
            freq: 180,
            dur: 0.22,
            type: "square"
        },
        {
            freq: 160,
            dur: 0.22,
            type: "square",
            gap: 0.04
        },
        {
            freq: 180,
            dur: 0.22,
            type: "square",
            gap: 0.04
        },
        {
            freq: 160,
            dur: 0.35,
            type: "square",
            gap: 0.04
        }
    ],
    gentle: [
        {
            freq: 392,
            dur: 0.5,
            type: "triangle"
        },
        {
            freq: 494,
            dur: 0.5,
            type: "triangle",
            gap: 0.12
        },
        {
            freq: 587,
            dur: 0.7,
            type: "triangle",
            gap: 0.12
        }
    ],
    siren: [
        {
            freq: 700,
            dur: 0.28,
            type: "sawtooth"
        },
        {
            freq: 500,
            dur: 0.28,
            type: "sawtooth",
            gap: 0.02
        },
        {
            freq: 700,
            dur: 0.28,
            type: "sawtooth",
            gap: 0.02
        },
        {
            freq: 500,
            dur: 0.28,
            type: "sawtooth",
            gap: 0.02
        },
        {
            freq: 700,
            dur: 0.35,
            type: "sawtooth",
            gap: 0.02
        }
    ]
};
let sharedCtx = null;
function getCtx() {
    if (!sharedCtx) {
        sharedCtx = new AudioContext();
    }
    return sharedCtx;
}
async function playAlarmSound(id, volume = 0.85, loops = 2) {
    const ctx = getCtx();
    if (ctx.state === "suspended") await ctx.resume();
    const pattern = PATTERNS[id] ?? PATTERNS.pulse;
    const master = ctx.createGain();
    master.gain.value = Math.max(0, Math.min(1, volume));
    master.connect(ctx.destination);
    let t = ctx.currentTime + 0.02;
    for(let loop = 0; loop < loops; loop++){
        for (const tone of pattern){
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = tone.type ?? "sine";
            osc.frequency.value = tone.freq;
            gain.gain.setValueAtTime(0.0001, t);
            gain.gain.exponentialRampToValueAtTime(0.55, t + 0.02);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + tone.dur);
            osc.connect(gain);
            gain.connect(master);
            osc.start(t);
            osc.stop(t + tone.dur + 0.02);
            t += tone.dur + (tone.gap ?? 0.06);
        }
        t += 0.25;
    }
    await new Promise((r)=>setTimeout(r, (t - ctx.currentTime + 0.1) * 1000));
}
function stopAlarmAudio() {
    if (sharedCtx) {
        void sharedCtx.close();
        sharedCtx = null;
    }
}
}),
"[project]/src/lib/storage.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "DEFAULT_SETTINGS",
    ()=>DEFAULT_SETTINGS,
    "exportBackup",
    ()=>exportBackup,
    "getNote",
    ()=>getNote,
    "importBackup",
    ()=>importBackup,
    "loadData",
    ()=>loadData,
    "overtimeForMonth",
    ()=>overtimeForMonth,
    "saveData",
    ()=>saveData,
    "setNote",
    ()=>setNote,
    "uid",
    ()=>uid
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/rota.ts [app-ssr] (ecmascript)");
;
const DEFAULT_SETTINGS = {
    hourlyRate: 18.5,
    overtimeMultiplier: 1.5,
    nightPremium: 0,
    currency: "GBP",
    wakeLeadMinutes: 90,
    dayWakeLeadMinutes: 90,
    nightWakeLeadMinutes: 90,
    alarmSound: "pulse",
    alarmVolume: 0.85,
    remindersEnabled: true,
    reminderTimes: [
        "17:00",
        "20:00"
    ],
    wakeAlarmsEnabled: true,
    shiftName: "B Shift",
    plantName: "Plastics"
};
const STORAGE_KEY = "plastics-b-shift-planner-v1";
function loadData() {
    if ("TURBOPACK compile-time truthy", 1) {
        return {
            settings: DEFAULT_SETTINGS,
            overtime: [],
            notes: [],
            adjustments: [],
            notificationPermissionAsked: false,
            installedHintDismissed: false
        };
    }
    //TURBOPACK unreachable
    ;
}
function saveData(data) {
    if ("TURBOPACK compile-time truthy", 1) return;
    //TURBOPACK unreachable
    ;
}
function uid() {
    return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}
function getNote(data, date) {
    const key = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])(date);
    return data.notes.find((n)=>n.dateKey === key)?.text ?? "";
}
function setNote(data, date, text) {
    const key = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$rota$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toDateKey"])(date);
    const notes = data.notes.filter((n)=>n.dateKey !== key);
    if (text.trim()) notes.push({
        dateKey: key,
        text: text.trim()
    });
    return {
        ...data,
        notes
    };
}
function overtimeForMonth(data, year, month) {
    const prefix = `${year}-${String(month + 1).padStart(2, "0")}`;
    return data.overtime.filter((o)=>o.dateKey.startsWith(prefix));
}
function exportBackup(data) {
    return JSON.stringify({
        version: 1,
        exportedAt: new Date().toISOString(),
        data
    }, null, 2);
}
function importBackup(json) {
    const parsed = JSON.parse(json);
    const data = "data" in parsed && parsed.data ? parsed.data : parsed;
    return {
        settings: {
            ...DEFAULT_SETTINGS,
            ...data.settings
        },
        overtime: data.overtime ?? [],
        notes: data.notes ?? [],
        adjustments: data.adjustments ?? [],
        notificationPermissionAsked: data.notificationPermissionAsked ?? false,
        installedHintDismissed: data.installedHintDismissed ?? false
    };
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__05c5l91._.js.map