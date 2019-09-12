var ML =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
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
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/ts/table.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/ts/table.ts":
/*!*************************!*\
  !*** ./src/ts/table.ts ***!
  \*************************/
/*! exports provided: SortTable */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"SortTable\", function() { return SortTable; });\nvar SortTable = /** @class */ (function () {\n    function SortTable(tableID) {\n        this.tableID = tableID;\n        this.table = null;\n        this.initialise();\n    }\n    SortTable.prototype.initialise = function () {\n        this.table = document.getElementById(this.tableID);\n        var headings = this.table.getElementsByTagName('th');\n        var tableIdentifier = this.tableID;\n        var sortFunction = this.sortColumnTable;\n        var _loop_1 = function (i) {\n            var heading = headings[i];\n            heading.onclick = function () {\n                sortFunction(tableIdentifier, i);\n            };\n        };\n        for (var i = 0; i < headings.length; i++) {\n            _loop_1(i);\n        }\n    };\n    /**\n     * Sorts a table column\n     * @param  {string} tableID\n     */\n    SortTable.prototype.sortColumnTable = function (tableID, columnID) {\n        var table;\n        var rows;\n        var switching = true;\n        var shouldSwitch;\n        var switchCount = 0;\n        var direction = \"ascending\";\n        var i, x, y;\n        table = document.getElementById(tableID);\n        switching = true;\n        while (switching) {\n            switching = false;\n            rows = table.rows;\n            for (i = 1; i < (rows.length - 1); i++) {\n                shouldSwitch = false;\n                x = rows[i].getElementsByTagName(\"TD\")[columnID];\n                y = rows[i + 1].getElementsByTagName(\"TD\")[columnID];\n                if (direction == \"ascending\") {\n                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {\n                        shouldSwitch = true;\n                        break;\n                    }\n                }\n                else if (direction == \"descending\") {\n                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {\n                        shouldSwitch = true;\n                        break;\n                    }\n                }\n            }\n            if (shouldSwitch) {\n                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);\n                switching = true;\n                switchCount++;\n            }\n            else {\n                if (switchCount == 0 && direction == \"ascending\") {\n                    direction = \"descending\";\n                    switching = true;\n                }\n            }\n        }\n    };\n    return SortTable;\n}());\n\n\n\n//# sourceURL=webpack://ML/./src/ts/table.ts?");

/***/ })

/******/ });