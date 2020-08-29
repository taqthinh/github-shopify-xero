module.exports =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = require('../ssr-module-cache.js');
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		var threw = true;
/******/ 		try {
/******/ 			modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 			threw = false;
/******/ 		} finally {
/******/ 			if(threw) delete installedModules[moduleId];
/******/ 		}
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./pages/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/@shopify/polaris/dist/styles.css":
/*!*******************************************************!*\
  !*** ./node_modules/@shopify/polaris/dist/styles.css ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiIuL25vZGVfbW9kdWxlcy9Ac2hvcGlmeS9wb2xhcmlzL2Rpc3Qvc3R5bGVzLmNzcy5qcyIsInNvdXJjZXNDb250ZW50IjpbXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///./node_modules/@shopify/polaris/dist/styles.css\n");

/***/ }),

/***/ "./node_modules/@shopify/polaris/locales/en.json":
/*!*******************************************************!*\
  !*** ./node_modules/@shopify/polaris/locales/en.json ***!
  \*******************************************************/
/*! exports provided: Polaris, default */
/***/ (function(module) {

eval("module.exports = JSON.parse(\"{\\\"Polaris\\\":{\\\"Avatar\\\":{\\\"label\\\":\\\"Avatar\\\",\\\"labelWithInitials\\\":\\\"Avatar with initials {initials}\\\"},\\\"Autocomplete\\\":{\\\"spinnerAccessibilityLabel\\\":\\\"Loading\\\"},\\\"Badge\\\":{\\\"PROGRESS_LABELS\\\":{\\\"incomplete\\\":\\\"Incomplete\\\",\\\"partiallyComplete\\\":\\\"Partially complete\\\",\\\"complete\\\":\\\"Complete\\\"},\\\"STATUS_LABELS\\\":{\\\"info\\\":\\\"Info\\\",\\\"success\\\":\\\"Success\\\",\\\"warning\\\":\\\"Warning\\\",\\\"critical\\\":\\\"Critical\\\",\\\"attention\\\":\\\"Attention\\\",\\\"new\\\":\\\"New\\\"}},\\\"Button\\\":{\\\"spinnerAccessibilityLabel\\\":\\\"Loading\\\",\\\"connectedDisclosureAccessibilityLabel\\\":\\\"Related actions\\\"},\\\"Common\\\":{\\\"checkbox\\\":\\\"checkbox\\\",\\\"undo\\\":\\\"Undo\\\",\\\"cancel\\\":\\\"Cancel\\\",\\\"newWindowAccessibilityHint\\\":\\\"(opens a new window)\\\",\\\"clear\\\":\\\"Clear\\\",\\\"close\\\":\\\"Close\\\",\\\"submit\\\":\\\"Submit\\\",\\\"more\\\":\\\"More\\\"},\\\"ContextualSaveBar\\\":{\\\"save\\\":\\\"Save\\\",\\\"discard\\\":\\\"Discard\\\"},\\\"DataTable\\\":{\\\"sortAccessibilityLabel\\\":\\\"sort {direction} by\\\",\\\"navAccessibilityLabel\\\":\\\"Scroll table {direction} one column\\\",\\\"totalsRowHeading\\\":\\\"Totals\\\",\\\"totalRowHeading\\\":\\\"Total\\\"},\\\"DatePicker\\\":{\\\"previousMonth\\\":\\\"Show previous month, {previousMonthName} {showPreviousYear}\\\",\\\"nextMonth\\\":\\\"Show next month, {nextMonth} {nextYear}\\\",\\\"today\\\":\\\"Today \\\",\\\"months\\\":{\\\"january\\\":\\\"January\\\",\\\"february\\\":\\\"February\\\",\\\"march\\\":\\\"March\\\",\\\"april\\\":\\\"April\\\",\\\"may\\\":\\\"May\\\",\\\"june\\\":\\\"June\\\",\\\"july\\\":\\\"July\\\",\\\"august\\\":\\\"August\\\",\\\"september\\\":\\\"September\\\",\\\"october\\\":\\\"October\\\",\\\"november\\\":\\\"November\\\",\\\"december\\\":\\\"December\\\"},\\\"days\\\":{\\\"monday\\\":\\\"Monday\\\",\\\"tuesday\\\":\\\"Tuesday\\\",\\\"wednesday\\\":\\\"Wednesday\\\",\\\"thursday\\\":\\\"Thursday\\\",\\\"friday\\\":\\\"Friday\\\",\\\"saturday\\\":\\\"Saturday\\\",\\\"sunday\\\":\\\"Sunday\\\"},\\\"daysAbbreviated\\\":{\\\"monday\\\":\\\"Mo\\\",\\\"tuesday\\\":\\\"Tu\\\",\\\"wednesday\\\":\\\"We\\\",\\\"thursday\\\":\\\"Th\\\",\\\"friday\\\":\\\"Fr\\\",\\\"saturday\\\":\\\"Sa\\\",\\\"sunday\\\":\\\"Su\\\"}},\\\"DiscardConfirmationModal\\\":{\\\"title\\\":\\\"Discard all unsaved changes\\\",\\\"message\\\":\\\"If you discard changes, you’ll delete any edits you made since you last saved.\\\",\\\"primaryAction\\\":\\\"Discard changes\\\",\\\"secondaryAction\\\":\\\"Continue editing\\\"},\\\"DropZone\\\":{\\\"overlayTextFile\\\":\\\"Drop file to upload\\\",\\\"overlayTextImage\\\":\\\"Drop image to upload\\\",\\\"errorOverlayTextFile\\\":\\\"File type is not valid\\\",\\\"errorOverlayTextImage\\\":\\\"Image type is not valid\\\",\\\"FileUpload\\\":{\\\"actionTitleFile\\\":\\\"Add file\\\",\\\"actionTitleImage\\\":\\\"Add image\\\",\\\"actionHintFile\\\":\\\"or drop files to upload\\\",\\\"actionHintImage\\\":\\\"or drop images to upload\\\",\\\"label\\\":\\\"Upload file\\\"}},\\\"EmptySearchResult\\\":{\\\"altText\\\":\\\"Empty search results\\\"},\\\"Frame\\\":{\\\"skipToContent\\\":\\\"Skip to content\\\",\\\"Navigation\\\":{\\\"closeMobileNavigationLabel\\\":\\\"Close navigation\\\"}},\\\"Icon\\\":{\\\"backdropWarning\\\":\\\"The {color} icon doesn’t accept backdrops. The icon colors that have backdrops are: {colorsWithBackDrops}\\\"},\\\"ActionMenu\\\":{\\\"RollupActions\\\":{\\\"rollupButton\\\":\\\"Actions\\\"}},\\\"Filters\\\":{\\\"moreFilters\\\":\\\"More filters\\\",\\\"moreFiltersWithCount\\\":\\\"More filters ({count})\\\",\\\"filter\\\":\\\"Filter {resourceName}\\\",\\\"noFiltersApplied\\\":\\\"No filters applied\\\",\\\"cancel\\\":\\\"Cancel\\\",\\\"done\\\":\\\"Done\\\",\\\"clearAllFilters\\\":\\\"Clear all filters\\\",\\\"clear\\\":\\\"Clear\\\",\\\"clearLabel\\\":\\\"Clear {filterName}\\\"},\\\"Modal\\\":{\\\"iFrameTitle\\\":\\\"body markup\\\",\\\"modalWarning\\\":\\\"These required properties are missing from Modal: {missingProps}\\\"},\\\"Pagination\\\":{\\\"previous\\\":\\\"Previous\\\",\\\"next\\\":\\\"Next\\\",\\\"pagination\\\":\\\"Pagination\\\"},\\\"ProgressBar\\\":{\\\"negativeWarningMessage\\\":\\\"Values passed to the progress prop shouldn’t be negative. Resetting {progress} to 0.\\\",\\\"exceedWarningMessage\\\":\\\"Values passed to the progress prop shouldn’t exceed 100. Setting {progress} to 100.\\\"},\\\"ResourceList\\\":{\\\"sortingLabel\\\":\\\"Sort by\\\",\\\"defaultItemSingular\\\":\\\"item\\\",\\\"defaultItemPlural\\\":\\\"items\\\",\\\"showing\\\":\\\"Showing {itemsCount} {resource}\\\",\\\"showingTotalCount\\\":\\\"Showing {itemsCount} of {totalItemsCount} {resource}\\\",\\\"loading\\\":\\\"Loading {resource}\\\",\\\"selected\\\":\\\"{selectedItemsCount} selected\\\",\\\"allItemsSelected\\\":\\\"All {itemsLength}+ {resourceNamePlural} in your store are selected.\\\",\\\"allFilteredItemsSelected\\\":\\\"All {itemsLength}+ {resourceNamePlural} in this filter are selected.\\\",\\\"selectAllItems\\\":\\\"Select all {itemsLength}+ {resourceNamePlural} in your store\\\",\\\"selectAllFilteredItems\\\":\\\"Select all {itemsLength}+ {resourceNamePlural} in this filter\\\",\\\"emptySearchResultTitle\\\":\\\"No {resourceNamePlural} found\\\",\\\"emptySearchResultDescription\\\":\\\"Try changing the filters or search term\\\",\\\"selectButtonText\\\":\\\"Select\\\",\\\"a11yCheckboxDeselectAllSingle\\\":\\\"Deselect {resourceNameSingular}\\\",\\\"a11yCheckboxSelectAllSingle\\\":\\\"Select {resourceNameSingular}\\\",\\\"a11yCheckboxDeselectAllMultiple\\\":\\\"Deselect all {itemsLength} {resourceNamePlural}\\\",\\\"a11yCheckboxSelectAllMultiple\\\":\\\"Select all {itemsLength} {resourceNamePlural}\\\",\\\"ariaLiveSingular\\\":\\\"{itemsLength} item\\\",\\\"ariaLivePlural\\\":\\\"{itemsLength} items\\\",\\\"Item\\\":{\\\"actionsDropdownLabel\\\":\\\"Actions for {accessibilityLabel}\\\",\\\"actionsDropdown\\\":\\\"Actions dropdown\\\",\\\"viewItem\\\":\\\"View details for {itemName}\\\"},\\\"BulkActions\\\":{\\\"actionsActivatorLabel\\\":\\\"Actions\\\",\\\"moreActionsActivatorLabel\\\":\\\"More actions\\\",\\\"warningMessage\\\":\\\"To provide a better user experience. There should only be a maximum of {maxPromotedActions} promoted actions.\\\"},\\\"FilterCreator\\\":{\\\"filterButtonLabel\\\":\\\"Filter\\\",\\\"selectFilterKeyPlaceholder\\\":\\\"Select a filter…\\\",\\\"addFilterButtonLabel\\\":\\\"Add filter\\\",\\\"showAllWhere\\\":\\\"Show all {resourceNamePlural} where:\\\"},\\\"FilterControl\\\":{\\\"textFieldLabel\\\":\\\"Search {resourceNamePlural}\\\"},\\\"FilterValueSelector\\\":{\\\"selectFilterValuePlaceholder\\\":\\\"Select a filter…\\\"},\\\"DateSelector\\\":{\\\"dateFilterLabel\\\":\\\"Select a value\\\",\\\"dateValueLabel\\\":\\\"Date\\\",\\\"dateValueError\\\":\\\"Match YYYY-MM-DD format\\\",\\\"dateValuePlaceholder\\\":\\\"YYYY-MM-DD\\\",\\\"SelectOptions\\\":{\\\"PastWeek\\\":\\\"in the last week\\\",\\\"PastMonth\\\":\\\"in the last month\\\",\\\"PastQuarter\\\":\\\"in the last 3 months\\\",\\\"PastYear\\\":\\\"in the last year\\\",\\\"ComingWeek\\\":\\\"next week\\\",\\\"ComingMonth\\\":\\\"next month\\\",\\\"ComingQuarter\\\":\\\"in the next 3 months\\\",\\\"ComingYear\\\":\\\"in the next year\\\",\\\"OnOrBefore\\\":\\\"on or before\\\",\\\"OnOrAfter\\\":\\\"on or after\\\"},\\\"FilterLabelForValue\\\":{\\\"past_week\\\":\\\"in the last week\\\",\\\"past_month\\\":\\\"in the last month\\\",\\\"past_quarter\\\":\\\"in the last 3 months\\\",\\\"past_year\\\":\\\"in the last year\\\",\\\"coming_week\\\":\\\"next week\\\",\\\"coming_month\\\":\\\"next month\\\",\\\"coming_quarter\\\":\\\"in the next 3 months\\\",\\\"coming_year\\\":\\\"in the next year\\\",\\\"on_or_before\\\":\\\"before {date}\\\",\\\"on_or_after\\\":\\\"after {date}\\\"}}},\\\"SkeletonPage\\\":{\\\"loadingLabel\\\":\\\"Page loading\\\"},\\\"Spinner\\\":{\\\"warningMessage\\\":\\\"The color {color} is not meant to be used on {size} spinners. The colors available on large spinners are: {colors}\\\"},\\\"Tabs\\\":{\\\"toggleTabsLabel\\\":\\\"More tabs\\\"},\\\"Tag\\\":{\\\"ariaLabel\\\":\\\"Remove {children}\\\"},\\\"TextField\\\":{\\\"characterCount\\\":\\\"{count} characters\\\",\\\"characterCountWithMaxLength\\\":\\\"{count} of {limit} characters used\\\"},\\\"TopBar\\\":{\\\"toggleMenuLabel\\\":\\\"Toggle menu\\\",\\\"SearchField\\\":{\\\"clearButtonLabel\\\":\\\"Clear\\\",\\\"search\\\":\\\"Search\\\"}},\\\"MediaCard\\\":{\\\"popoverButton\\\":\\\"Actions\\\"},\\\"VideoThumbnail\\\":{\\\"playButtonA11yLabel\\\":{\\\"default\\\":\\\"Play video\\\",\\\"defaultWithDuration\\\":\\\"Play video of length {duration}\\\",\\\"duration\\\":{\\\"hours\\\":{\\\"other\\\":{\\\"only\\\":\\\"{hourCount} hours\\\",\\\"andMinutes\\\":\\\"{hourCount} hours and {minuteCount} minutes\\\",\\\"andMinute\\\":\\\"{hourCount} hours and {minuteCount} minute\\\",\\\"minutesAndSeconds\\\":\\\"{hourCount} hours, {minuteCount} minutes, and {secondCount} seconds\\\",\\\"minutesAndSecond\\\":\\\"{hourCount} hours, {minuteCount} minutes, and {secondCount} second\\\",\\\"minuteAndSeconds\\\":\\\"{hourCount} hours, {minuteCount} minute, and {secondCount} seconds\\\",\\\"minuteAndSecond\\\":\\\"{hourCount} hours, {minuteCount} minute, and {secondCount} second\\\",\\\"andSeconds\\\":\\\"{hourCount} hours and {secondCount} seconds\\\",\\\"andSecond\\\":\\\"{hourCount} hours and {secondCount} second\\\"},\\\"one\\\":{\\\"only\\\":\\\"{hourCount} hour\\\",\\\"andMinutes\\\":\\\"{hourCount} hour and {minuteCount} minutes\\\",\\\"andMinute\\\":\\\"{hourCount} hour and {minuteCount} minute\\\",\\\"minutesAndSeconds\\\":\\\"{hourCount} hour, {minuteCount} minutes, and {secondCount} seconds\\\",\\\"minutesAndSecond\\\":\\\"{hourCount} hour, {minuteCount} minutes, and {secondCount} second\\\",\\\"minuteAndSeconds\\\":\\\"{hourCount} hour, {minuteCount} minute, and {secondCount} seconds\\\",\\\"minuteAndSecond\\\":\\\"{hourCount} hour, {minuteCount} minute, and {secondCount} second\\\",\\\"andSeconds\\\":\\\"{hourCount} hour and {secondCount} seconds\\\",\\\"andSecond\\\":\\\"{hourCount} hour and {secondCount} second\\\"}},\\\"minutes\\\":{\\\"other\\\":{\\\"only\\\":\\\"{minuteCount} minutes\\\",\\\"andSeconds\\\":\\\"{minuteCount} minutes and {secondCount} seconds\\\",\\\"andSecond\\\":\\\"{minuteCount} minutes and {secondCount} second\\\"},\\\"one\\\":{\\\"only\\\":\\\"{minuteCount} minute\\\",\\\"andSeconds\\\":\\\"{minuteCount} minute and {secondCount} seconds\\\",\\\"andSecond\\\":\\\"{minuteCount} minute and {secondCount} second\\\"}},\\\"seconds\\\":{\\\"other\\\":\\\"{secondCount} seconds\\\",\\\"one\\\":\\\"{secondCount} second\\\"}}}}}}\");//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiIuL25vZGVfbW9kdWxlcy9Ac2hvcGlmeS9wb2xhcmlzL2xvY2FsZXMvZW4uanNvbi5qcyIsInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///./node_modules/@shopify/polaris/locales/en.json\n");

/***/ }),

/***/ "./pages/index.js":
/*!************************!*\
  !*** ./pages/index.js ***!
  \************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _shopify_polaris__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @shopify/polaris */ \"@shopify/polaris\");\n/* harmony import */ var _shopify_polaris__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_shopify_polaris__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom */ \"react-dom\");\n/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _shopify_polaris_dist_styles_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @shopify/polaris/dist/styles.css */ \"./node_modules/@shopify/polaris/dist/styles.css\");\n/* harmony import */ var _shopify_polaris_dist_styles_css__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_shopify_polaris_dist_styles_css__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _shopify_polaris_locales_en_json__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @shopify/polaris/locales/en.json */ \"./node_modules/@shopify/polaris/locales/en.json\");\nvar _shopify_polaris_locales_en_json__WEBPACK_IMPORTED_MODULE_4___namespace = /*#__PURE__*/__webpack_require__.t(/*! @shopify/polaris/locales/en.json */ \"./node_modules/@shopify/polaris/locales/en.json\", 1);\nvar _jsxFileName = \"/home/thinh/Documents/odoo-13/customaddons/shopify_app/app/pages/index.js\";\nvar __jsx = react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement;\n\n\n\n\n // import image from './connector.png';\n\nclass Main extends react__WEBPACK_IMPORTED_MODULE_1__[\"Component\"] {\n  constructor(props) {\n    super(props);\n  }\n\n  render() {\n    return __jsx(_shopify_polaris__WEBPACK_IMPORTED_MODULE_0__[\"AppProvider\"], {\n      i18n: _shopify_polaris_locales_en_json__WEBPACK_IMPORTED_MODULE_4__,\n      __self: this,\n      __source: {\n        fileName: _jsxFileName,\n        lineNumber: 16,\n        columnNumber: 13\n      }\n    }, __jsx(_shopify_polaris__WEBPACK_IMPORTED_MODULE_0__[\"Frame\"], {\n      __self: this,\n      __source: {\n        fileName: _jsxFileName,\n        lineNumber: 17,\n        columnNumber: 17\n      }\n    }, __jsx(_shopify_polaris__WEBPACK_IMPORTED_MODULE_0__[\"Page\"], {\n      __self: this,\n      __source: {\n        fileName: _jsxFileName,\n        lineNumber: 18,\n        columnNumber: 21\n      }\n    }, __jsx(\"img\", {\n      src: \"connector.png\",\n      alt: \"Connect to Xero\",\n      width: \"100%\",\n      height: \"100%\",\n      __self: this,\n      __source: {\n        fileName: _jsxFileName,\n        lineNumber: 19,\n        columnNumber: 25\n      }\n    }), __jsx(_shopify_polaris__WEBPACK_IMPORTED_MODULE_0__[\"Button\"], {\n      onClick: event => window.top.location.href = \"/xero_connect\",\n      primary: true,\n      __self: this,\n      __source: {\n        fileName: _jsxFileName,\n        lineNumber: 20,\n        columnNumber: 25\n      }\n    }, \"Save Settings\"))));\n  }\n\n}\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (Main); // const wrapper = document.getElementById(\"xero_connect\");\n// wrapper ? ReactDOM.render(<Main />, wrapper) : false;//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vLi9wYWdlcy9pbmRleC5qcz80NGQ4Il0sIm5hbWVzIjpbIk1haW4iLCJDb21wb25lbnQiLCJjb25zdHJ1Y3RvciIsInByb3BzIiwicmVuZGVyIiwidHJhbnNsYXRpb25zIiwiZXZlbnQiLCJ3aW5kb3ciLCJ0b3AiLCJsb2NhdGlvbiIsImhyZWYiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtDQUVBOztBQUVBLE1BQU1BLElBQU4sU0FBbUJDLCtDQUFuQixDQUE0QjtBQUV4QkMsYUFBVyxDQUFDQyxLQUFELEVBQVE7QUFDZixVQUFNQSxLQUFOO0FBQ0g7O0FBRURDLFFBQU0sR0FBRztBQUNMLFdBQ0ksTUFBQyw0REFBRDtBQUFhLFVBQUksRUFBRUMsNkRBQW5CO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FDSSxNQUFDLHNEQUFEO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FDSSxNQUFDLHFEQUFEO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsT0FDSTtBQUFLLFNBQUcsRUFBQyxlQUFUO0FBQXlCLFNBQUcsRUFBQyxpQkFBN0I7QUFBK0MsV0FBSyxFQUFDLE1BQXJEO0FBQTRELFlBQU0sRUFBQyxNQUFuRTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBLE1BREosRUFFSSxNQUFDLHVEQUFEO0FBQVEsYUFBTyxFQUFFQyxLQUFLLElBQUtDLE1BQU0sQ0FBQ0MsR0FBUCxDQUFXQyxRQUFYLENBQW9CQyxJQUFwQixHQUF5QixlQUFwRDtBQUFxRSxhQUFPLE1BQTVFO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsdUJBRkosQ0FESixDQURKLENBREo7QUFVSDs7QUFqQnVCOztBQW9CYlYsbUVBQWYsRSxDQUVBO0FBQ0EiLCJmaWxlIjoiLi9wYWdlcy9pbmRleC5qcy5qcyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IFRodW1ibmFpbCwgQnV0dG9uLE1lZGlhQ2FyZCwgRnJhbWUsRm9ybUxheW91dCwgTGF5b3V0LCBQYWdlLCBBcHBQcm92aWRlciB9IGZyb20gJ0BzaG9waWZ5L3BvbGFyaXMnO1xuaW1wb3J0IFJlYWN0LCB7Q29tcG9uZW50fSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgUmVhY3RET00gZnJvbSBcInJlYWN0LWRvbVwiO1xuaW1wb3J0ICdAc2hvcGlmeS9wb2xhcmlzL2Rpc3Qvc3R5bGVzLmNzcyc7XG5pbXBvcnQgdHJhbnNsYXRpb25zIGZyb20gJ0BzaG9waWZ5L3BvbGFyaXMvbG9jYWxlcy9lbi5qc29uJztcbi8vIGltcG9ydCBpbWFnZSBmcm9tICcuL2Nvbm5lY3Rvci5wbmcnO1xuXG5jbGFzcyBNYWluIGV4dGVuZHMgQ29tcG9uZW50e1xuXG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxBcHBQcm92aWRlciBpMThuPXt0cmFuc2xhdGlvbnN9PlxuICAgICAgICAgICAgICAgIDxGcmFtZT5cbiAgICAgICAgICAgICAgICAgICAgPFBhZ2U+XG4gICAgICAgICAgICAgICAgICAgICAgICA8aW1nIHNyYz1cImNvbm5lY3Rvci5wbmdcIiBhbHQ9XCJDb25uZWN0IHRvIFhlcm9cIiB3aWR0aD1cIjEwMCVcIiBoZWlnaHQ9XCIxMDAlXCIgLz5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxCdXR0b24gb25DbGljaz17ZXZlbnQgPT4gIHdpbmRvdy50b3AubG9jYXRpb24uaHJlZj1cIi94ZXJvX2Nvbm5lY3RcIn0gcHJpbWFyeT5TYXZlIFNldHRpbmdzPC9CdXR0b24+XG4gICAgICAgICAgICAgICAgICAgIDwvUGFnZT5cbiAgICAgICAgICAgICAgICA8L0ZyYW1lPlxuICAgICAgICAgICAgPC9BcHBQcm92aWRlcj5cbiAgICAgICAgKVxuICAgIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgTWFpbjtcblxuLy8gY29uc3Qgd3JhcHBlciA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKFwieGVyb19jb25uZWN0XCIpO1xuLy8gd3JhcHBlciA/IFJlYWN0RE9NLnJlbmRlcig8TWFpbiAvPiwgd3JhcHBlcikgOiBmYWxzZTtcblxuXG5cblxuXG4iXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///./pages/index.js\n");

/***/ }),

/***/ "@shopify/polaris":
/*!***********************************!*\
  !*** external "@shopify/polaris" ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"@shopify/polaris\");//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vZXh0ZXJuYWwgXCJAc2hvcGlmeS9wb2xhcmlzXCI/YTYyMyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQSIsImZpbGUiOiJAc2hvcGlmeS9wb2xhcmlzLmpzIiwic291cmNlc0NvbnRlbnQiOlsibW9kdWxlLmV4cG9ydHMgPSByZXF1aXJlKFwiQHNob3BpZnkvcG9sYXJpc1wiKTsiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///@shopify/polaris\n");

/***/ }),

/***/ "react":
/*!************************!*\
  !*** external "react" ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"react\");//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vZXh0ZXJuYWwgXCJyZWFjdFwiPzU4OGUiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEiLCJmaWxlIjoicmVhY3QuanMiLCJzb3VyY2VzQ29udGVudCI6WyJtb2R1bGUuZXhwb3J0cyA9IHJlcXVpcmUoXCJyZWFjdFwiKTsiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///react\n");

/***/ }),

/***/ "react-dom":
/*!****************************!*\
  !*** external "react-dom" ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"react-dom\");//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vZXh0ZXJuYWwgXCJyZWFjdC1kb21cIj81ZTlhIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBIiwiZmlsZSI6InJlYWN0LWRvbS5qcyIsInNvdXJjZXNDb250ZW50IjpbIm1vZHVsZS5leHBvcnRzID0gcmVxdWlyZShcInJlYWN0LWRvbVwiKTsiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///react-dom\n");

/***/ })

/******/ });