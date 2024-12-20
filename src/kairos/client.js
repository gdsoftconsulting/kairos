// 
//    This file is part of Kairos.
//
//    Kairos is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    Kairos is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with Kairos.  If not, see <http://www.gnu.org/licenses/>.
//

/*jshint esversion: 6 */

let VERSION = "@@VERSION@@";
let desktop = {};
desktop.variables = {};
desktop.current = {};
let ajaxcpt = 0;

let log = log4javascript.getLogger('CLIENT ');
let appender = new log4javascript.BrowserConsoleAppender();
let popUpLayout = new log4javascript.PatternLayout("%d{HH:mm:ss.SSS} %-5p %-7c - %m%n");
appender.setLayout(popUpLayout);
log.addAppender(appender);
log.info('KAIROS V' + VERSION);

document.onkeydown = function (e) {
    e = e || window.event;
    desktop.keydown = e;
};

document.onclick = function (e) {
    e = e || window.event;
    desktop.mouseevent = e;
};

document.ondblclick = function (e) {
    e = e || window.event;
    desktop.mouseevent = e;
};

document.onmousedown = function (e) {
    e = e || window.event;
    desktop.mouseevent = e;
    desktop.click = null;
};

document.onmouseup = function (e) {
    e = e || window.event;
    desktop.mouseevent = e;
    desktop.click = e;
};

dhtmlXLayoutCell.prototype.setBI = function(url){
    let cont = this.cell.childNodes[this.conf.idx.cont];
    cont.style.backgroundImage = `url(${url})`;
    cont.style.backgroundSize = "100% 100%";
    cont = null;
};

dhtmlXWindowsCell.prototype.setBI = function(url){
    let cont = this.cell.childNodes[this.conf.idx.cont];
    cont.style.backgroundImage = `url(${url})`;
    cont.style.backgroundSize = "100% 100%";
    cont = null;
};


// dhtmlXWindowsCell.prototype.setBC = function(color){
//     let cont = this.cell.childNodes[this.conf.idx.cont];
//     cont.style.backgroundColor = color;
//     cont = null;
// };

dhtmlXForm.prototype.cross_and_load = function(data, top){
    this.loadStruct(data);
    this.base[0].style.position = "absolute";
    this.base[0].style.width = "auto";
    this.base[0].style.marginLeft = `${-Math.round(this.base[0].offsetWidth/2)}px`;
    this.base[0].style.left = "50%";
};

dhtmlXTreeView.prototype.refreshItem = function(id){
    let me = this;
    if (id !== undefined) {
        _.each(me.getSubItems(id), function (e) {
            me.deleteItem(e);
        });
        me.loadStruct(`gettree?nodesdb=${desktop.settings.nodesdb}&id=${id}`);
    }
};

dhtmlXTreeView.prototype.getPath = function(id){
    let me = this;
    let parent = me.getParentId(id);
    return parent === undefined ? me.getItemText(id) === "/" ? "" : me.getItemText(id) : me.getPath(parent) + '/' + me.getItemText(id);
};

let makeURL = function (s, p) {
    let esc = encodeURIComponent;
    let query = Object.keys(p).map(k => esc(k) + '=' + esc(p[k])).join('&');
    return query === '' ? s : s + '?' + query;
};

let microAjax = function (options) {
    if (!options.method) {
        options.method = "GET";
    }
    let noop = function () {};
    if (!options.success) {
        options.success = noop;
    }
    if (!options.warning) {
        options.warning = noop;
    }
    if (!options.error) {
        options.error = noop;
    }
    let request = new XMLHttpRequest();
    request.onload = function() {
        if (request.readyState === 4 && request.status === 200) {
            options.success(request.responseText);
        } else {
            options.warning(request);
        }
    };
    request.onerror = options.error;
    if (options.method === 'GET') {
        request.open(options.method, makeURL(options.url, options.data), true);
        request.send(undefined);
    } else {
        request.open(options.method, options.url, true);
        let boundary = "-------------------Separator";
        request.setRequestHeader("Content-Type","multipart/form-data; boundary=" + boundary);
        let stream = '';
        _.each(options.data, function(v, k) {
            stream += '--' + boundary + '\r\n' + 'Content-Disposition: form-data; name="' + k + '"\r\n\r\n' + v + '\r\n';
        });
        stream += '--' + boundary + '--';
        request.send(stream);
    }
};

let genajax = function (method, type) {
    let h = function (s, p) {
        let f = function (next) {
            let logging = desktop.settings === undefined ? 'info' : desktop.settings.logging;
            if (p === undefined) {
                p = {logging: logging};
            } else {
                p.logging = p.logging === undefined ? logging : p.logging;
            }
            ajaxcpt += 1;
            desktop.statusbar.setText("AJAX call running ...");
            desktop.statusbar.style.backgroundColor = "coral";
            let ferror = function (result) {
                ajaxcpt -= 1;
                if (ajaxcpt === 0) {
                    log.error(`### METHOD: ${method}, URL: ${s}...`);
                    desktop.statusbar.setText("");
                    desktop.statusbar.style.backgroundColor = "lightskyblue";
                }
                return next("Kairos server connection error!");
            };
            let fwarn = function (result) {
                ajaxcpt -= 1;
                if (ajaxcpt === 0) {
                    log.warn(`!!! METHOD: ${method}, URL: ${s}...`);
                    desktop.statusbar.setText("");
                    desktop.statusbar.style.backgroundColor = "lightskyblue";
                }
                return next(`Kairos server returned: ${result.status}, ${result.statusText}`);
            };
            let fdone = function (result) {
                result = JSON.parse(result);
                ajaxcpt -= 1;
                if (ajaxcpt === 0) {
                    desktop.statusbar.setText("");
                    desktop.statusbar.style.backgroundColor = "lightskyblue";
                }
                log.info(`<<< METHOD: ${method}, URL: ${s}...`);
                if (!result.success) {
                    return next(result.message);
                }
                return next(null, result.data);
            };
            log.info(`>>> METHOD: ${method}, URL: ${s}...`);
            microAjax({url: s, data: p, method: method, success: fdone, warning: fwarn, error: ferror});
        };
        let g = function(_, next) {
            f(next);
        };
        return type === 'first' ? f : g;
    };
    return h;
};

let ajax_get_first_in_async_waterfall = genajax("GET", "first");
let ajax_post_first_in_async_waterfall = genajax("POST", "first");
let ajax_get_in_async_parallel = genajax("GET", "first");
let ajax_get_next_in_async_waterfall = genajax("GET", "next");

let waterfall = function (a, fposterr) {
    async.waterfall(a, function (err, result) {
        if (err) {
            alertify.error('<div style="font-size:150%;">' + err + "</div>", 20000);
            if (fposterr !== undefined) {
                fposterr();
            }
        }
    });
};

let parallel = function (o, callback) {
    async.parallel(o, function (err, results) {
        if (err) {
            alertify.error('<div style="font-size:150%;">' + err + "</div>", 20000);
        } else {
            callback(results);
        }
    });
};

let getallusers = function (data) {
    let result = [];
    _.each(data, function (x) {
        result.push({id: x._id, value: x.user});
    });
    return result;
};

let getallroles = function (data) {
    let result = [];
    _.each(data, function (x) {
        result.push({id: x._id, value: x.role});
    });
    return result;
};

let getallgrants = function (x) {
    let result = [];
    _.each(x, function (g) {
        result.push({id: g._id, user: g.user, role: g.role});
    });
    return result;
};

let getallsystemdb = function (data) {
    let result = [];
    _.each(data, function (s) {
        result.push({id: s.name, value: s.name});
    });
    return result;
};

let getallnodesdb = function (data) {
    let result = [];
    _.each(data, function (s) {
        result.push({id: s.name, value: s.name});
    });
    return result;
};

let getalltemplates = function (data) {
    let result = [];
    _.each(data, function (t) {
        result.push({id: t.id, value: t.id});
    });
    return _.uniq(result);
};

let getallwallpapers = function (data) {
    let result = [];
    _.each(data, function (t) {
        result.push({id: t.id, value: t.id});
    });
    return _.uniq(result);
};

let getallcolors = function (data) {
    let result = [];
    _.each(data, function (t) {
        result.push({id: t.id, value: t.id});
    });
    return _.uniq(result);
};

let getallobjects = function (data) {
    let result = [];
    let idx = {};
    let iv = -1;
    _.each(data, function (x) {
        if (idx[x.origin] === undefined) {
            iv = iv + 1;
            idx[x.origin] = iv;
        }
        result.push({id: idx[x.origin] + '/' + x.rid, name: x.id, type: x.type, created: x.created, origin: x.origin});
    });
    return result;
};

let getalldatabases = function (data) {
    let result = [];
    _.each(data, function (x) {
        let size = x.size / 1024;
        result.push({id: x.name, size: size.toFixed(3)});
    });
    return result;
};

let getallchoices = function (data, type) {
    let result = [];
    if (type === "C") {
        _.each(data, function (array) {
            _.each(array, function (c) {
                result.push(c.label);
            });
        });
    } else {
        _.each(data, function (c) {
            result.push(c.label);
        });
    }
    return _.uniq(result);
};

let gensubmenus = function (menu, items, parentid, node) {
    let cpt = 0;
    let previousid = null;
    _.each(items, function (i) {
        let id = parentid + '_' + cpt;
        if (_.contains(_.keys(node.datasource.collections), i.tablecondition) || i.tablecondition === undefined) {
            if (i.type === 'separator') {
                if (previousid !== null) {
                    menu.addNewSeparator(previousid, id);
                }
            }
            if (i.type === 'menuitem') {
                menu.addNewChild(parentid, undefined, id, i.label);
                menu.actions[id] = {action: i.action, chart: i.chart, choice: i.choice, layout: i.layout, keyfunc: i.keyfunc};
                previousid = id;
            }
            if (i.type === 'submenu') {
                menu.addNewChild(parentid, undefined, id, i.label);
                gensubmenus(menu, i.items, id, node);
                previousid = id;
            }
            cpt += 1;
        }
    });
};

let getcollections = function (node) {
    let result = [];
    _.each(node.datasource.collections, function (x, k) {
        if (node.datasource.cache === undefined || node.datasource.cache.collections === undefined || node.datasource.cache.collections[k] === undefined) {
            result.push({id: k, collection: k, analyzer: x.analyzer, partition: "", created: ""});
        } else {
            _.each(node.datasource.cache.collections[k], function (y, p) {
                result.push({id: k + '_' + p, collection: k, analyzer: x.analyzer, partition: p, created: node.datasource.cache.collections[k][p]});
            });
        }
    });
    return result;
};

let mxg_createPopupMenu = function (graph, menu, cell, evt) {
    let model = graph.getModel();
    if (cell != null) {
        if (model.isVertex(cell)) {
            if (cell.attributes.specimen === 'CHART') {
                menu.addItem('Add Yaxis', 'resources/mxgraph/images/plus.png', function() {
                    mxg_addChild(graph, cell, 'YAXIS');
                });
                menu.addItem('Edit Id', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'id';
                    cell.value = cell.attributes.id;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Title', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'title';
                    cell.value = cell.attributes.title;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Subtitle', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'subtitle';
                    cell.value = cell.attributes.subtitle;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Reftime', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'reftime';
                    cell.value = cell.attributes.reftime;
                    graph.startEditingAtCell(cell);
                });
            }
            if (cell.attributes.specimen === 'YAXIS') {
                menu.addItem('Add Renderer', 'resources/mxgraph/images/plus.png', function() {
                    mxg_addChild(graph, cell, 'RENDERER');
                });
                menu.addItem('Edit Title', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'title';
                    cell.value = cell.attributes.title;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Scaling', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'scaling';
                    cell.value = cell.attributes.scaling;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Position', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'position';
                    cell.value = cell.attributes.position;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Properties', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'properties';
                    cell.value = cell.attributes.properties;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Minvalue', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'minvalue';
                    cell.value = cell.attributes.minvalue;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Maxvalue', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'maxvalue';
                    cell.value = cell.attributes.maxvalue;
                    graph.startEditingAtCell(cell);
                });
            }
            if (cell.attributes.specimen === 'RENDERER') {
                menu.addItem('Add Query', 'resources/mxgraph/images/plus.png', function() {
                    mxg_addChild(graph, cell, 'QUERY');
                });
                menu.addItem('Edit Type', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'type';
                    cell.value = cell.attributes.type;
                    graph.startEditingAtCell(cell);
                });
            }
            if (cell.attributes.specimen === 'DATASET') {
                menu.addItem('Add Dataset piece', 'resources/mxgraph/images/plus.png', function() {
                    mxg_addChild(graph, cell, 'PIECE');
                });
                menu.addItem('Edit Groupby', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'groupby';
                    cell.value = cell.attributes.groupby;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Projection', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'projection';
                    cell.value = cell.attributes.projection;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Collections', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'collections';
                    cell.value = cell.attributes.collections;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Userfunctions', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'userfunctions';
                    cell.value = cell.attributes.userfunctions;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Info', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'info';
                    cell.value = cell.attributes.info;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Onclick', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'onclick';
                    cell.value = cell.attributes.onclick;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Filterable', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'filterable';
                    cell.value = cell.attributes.filterable;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Nocache', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'nocache';
                    cell.value = cell.attributes.nocache;
                    graph.startEditingAtCell(cell);
                });
            }
            if (cell.attributes.specimen === 'PIECE') {
                menu.addItem('Edit Table', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'table';
                    cell.value = cell.attributes.table;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Projection', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'projection';
                    cell.value = cell.attributes.projection;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Restriction', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'restriction';
                    cell.value = cell.attributes.restriction;
                    graph.startEditingAtCell(cell);
                });
                menu.addItem('Edit Value', 'resources/mxgraph/images/edit.png', function() {
                    graph.attributes.current = cell;
                    graph.attributes.edited = 'value';
                    cell.value = cell.attributes.value;
                    graph.startEditingAtCell(cell);
                });
            }
        }
        if (cell.id != 'root' && model.isVertex(cell)) {
            menu.addItem('Delete', 'resources/mxgraph/images/delete.png', function() {
                mxg_deleteSubtree(graph, cell);
            });
        }
    } else {
        menu.addItem('Fit', 'resources/mxgraph/images/fit.png', function() {
            graph.fit();
        });
        menu.addItem('Actual', 'resources/mxgraph/images/actual.png', function() {
            graph.zoomActual();
        });
        menu.addItem('Zoom in', 'resources/mxgraph/images/zoomin.png', function() {
            graph.zoomIn();
        });
        menu.addItem('Zoom out', 'resources/mxgraph/images/zoomout.png', function() {
            graph.zoomOut();
        });
        menu.addSeparator();
        menu.addItem('Print', 'resources/mxgraph/images/printpreview.png', function() {
            let preview = new mxPrintPreview(graph, 1);
            preview.open();
        });
        menu.addItem('Poster Print', 'resources/mxgraph/images/printpreview.png', function()	{
            let pageCount = mxUtils.prompt('Enter maximum page count', '1');
            if (pageCount != null) {
                let scale = mxUtils.getScaleForPageCount(pageCount, graph);
                let preview = new mxPrintPreview(graph, scale);
                preview.open();
            }
        });
    }
};

let mxg_addOverlays = function (graph, cell, addPlusIcon, addDeleteIcon, addCloneIcon) {
    let overlay;
    if (addPlusIcon) {
        let text = cell.attributes.specimen === 'CHART' ? 'Add Yaxis' : cell.attributes.specimen === 'YAXIS' ? 'Add Renderer' : cell.attributes.specimen === 'RENDERER' ? 'Add Dataset' : 'Add Dataset Piece';
        overlay = new mxCellOverlay(new mxImage('resources/mxgraph/images/plus.png', 24, 24), text);
        overlay.cursor = 'hand';
        overlay.align = mxConstants.ALIGN_CENTER;
        overlay.addListener(mxEvent.CLICK, mxUtils.bind(this, function(sender, evt) {
            let specimen = cell.attributes.specimen === 'CHART' ? 'YAXIS' : cell.attributes.specimen === 'YAXIS' ? 'RENDERER' : cell.attributes.specimen === 'RENDERER' ? 'DATASET' : 'PIECE';
            mxg_addChild(graph, cell, specimen);
        }));
        graph.addCellOverlay(cell, overlay);
    }
    if (addDeleteIcon) {
        overlay = new mxCellOverlay(new mxImage('resources/mxgraph/images/delete.png', 24, 24), 'Delete');
        overlay.cursor = 'hand';
        overlay.offset = new mxPoint(0, 12);
        overlay.align = mxConstants.ALIGN_CENTER;
        overlay.verticalAlign = mxConstants.ALIGN_TOP;
        overlay.addListener(mxEvent.CLICK, mxUtils.bind(this, function(sender, evt) {
            mxg_deleteSubtree(graph, cell);
        }));
        graph.addCellOverlay(cell, overlay);
    }
    if (addCloneIcon) {
        overlay = new mxCellOverlay(new mxImage('resources/mxgraph/images/end.png', 24, 24), 'Clone');
        overlay.cursor = 'hand';
        overlay.offset = new mxPoint(-12, 0);
        overlay.align = mxConstants.ALIGN_RIGHT;
        overlay.verticalAlign = mxConstants.ALIGN_MIDDLE;
        overlay.addListener(mxEvent.CLICK, mxUtils.bind(this, function(sender, evt) {
            mxg_cloneSubtree(graph, cell);
        }));
        graph.addCellOverlay(cell, overlay);
    }
};

let mxg_addChild = function (graph, cell, specimen) {
    let parent = graph.getDefaultParent();
    let vertex;
    graph.getModel().beginUpdate();
    try {
        vertex = graph.insertVertex(parent, null, specimen);
        vertex.attributes = {'specimen': specimen};
        if (vertex.attributes.specimen === 'YAXIS') {
            vertex.attributes.title = '"TITLE to be defined"';
            vertex.attributes.scaling = '"LINEAR"';
            vertex.attributes.position = '"LEFT"';
            vertex.attributes.properties = '{}';
            vertex.attributes.minvalue = 'null';
            vertex.attributes.maxvalue = 'null';
        }
        if (vertex.attributes.specimen === 'RENDERER') {
            vertex.attributes.type = '"L"';
        }
        if (vertex.attributes.specimen === 'DATASET') {
            vertex.attributes.groupby = '"sum"';
            vertex.attributes.projection = '"label"';
            vertex.attributes.collections = '[]';
            vertex.attributes.userfunctions = '[]';
            vertex.attributes.info = '{}';
            vertex.attributes.onclick = '{}';
            vertex.attributes.filterable = 'true';
            vertex.attributes.nocache = 'false';
        }
        if (vertex.attributes.specimen === 'PIECE') {
            vertex.attributes.table = '"UNKNOWN_TABLE"';
            vertex.attributes.projection = '"UNKNOWN_COLUMN"';
            vertex.attributes.restriction = '""';
            vertex.attributes.value = '"UNKNOWN_VALUE"';
        }
        vertex.value = mxg_setValue(vertex);
        let geometry = graph.getModel().getGeometry(vertex);
        let size = graph.getPreferredSizeForCell(vertex);
        geometry.width = size.width;
        geometry.height = size.height;
        let edge = graph.insertEdge(parent, null, '', cell, vertex);
        edge.geometry.x = 1;
        edge.geometry.y = 0;
        edge.geometry.offset = new mxPoint(0, -20);
        mxg_addOverlays(graph, vertex, vertex.attributes.specimen === 'PIECE' ? false : true, true, true);
    }
    finally {
        graph.getModel().endUpdate();
        graph.scrollCellToVisible(vertex, true);
    }
    return vertex;
};
    
let mxg_deleteSubtree = function (graph, cell) {
    let cells = [];
    graph.traverse(cell, true, function(vertex)
    {
        cells.push(vertex);
        return true;
    });
    graph.removeCells(cells);
};

let mxg_cloneSubtree = function (graph, cell) {
    let parent = graph.getDefaultParent();
    let tome = null;
    _.each(cell.edges, function (e) {
        if (cell.id === e.target.id) {
            tome = e;
        }
    });
    let clones = {};
    graph.getModel().beginUpdate();
    try {
        graph.traverse(cell, true, function (vertex, edge) {
            let from = edge === undefined ? tome.source : clones[edge.source.id];
            let clonevertex = mxg_addChild(graph, from, vertex.attributes.specimen);
            clonevertex.attributes = {};
            _.each(vertex.attributes, function (v, k) {
                clonevertex.attributes[k] = v;
            });
            clonevertex.value = mxg_setValue(clonevertex);
            graph.updateCellSize(clonevertex);
            clonevertex.setStyle(vertex.getStyle());
            clones[vertex.id] = clonevertex;

        });
    }
    finally {
        graph.getModel().endUpdate();
        graph.scrollCellToVisible(clones[cell.id], true);
    }
};

let mxg_setValue = function (cell) {
    let r = cell.attributes.specimen + '\n\n' + (cell.attributes.specimen === 'CHART' ? 'id: ' + cell.attributes.id + '\n' + 'title: ' + cell.attributes.title + '\n' + 'subtitle: ' + cell.attributes.subtitle + '\n' + 'reftime: ' + cell.attributes.reftime :
                    cell.attributes.specimen === 'YAXIS' ? 'title: ' + cell.attributes.title + '\n' + 'scaling: ' + cell.attributes.scaling + '\n' + 'position: ' + cell.attributes.position + '\n' + 'properties: ' + cell.attributes.properties + '\n' + 'minvalue: ' + cell.attributes.minvalue + '\n' + 'maxvalue: ' + cell.attributes.maxvalue  :
                    cell.attributes.specimen === 'RENDERER' ? 'type: ' + cell.attributes.type :
                    cell.attributes.specimen === 'DATASET' ? 'groupby: ' + cell.attributes.groupby + '\n' + 'projection: ' + cell.attributes.projection + '\n' + 'collections: ' + cell.attributes.collections + '\n' + 'userfunctions: ' + cell.attributes.userfunctions+ '\n' + 'info: ' + cell.attributes.info + '\n' + 'onclick: ' + cell.attributes.onclick + '\n' + 'filterable: ' + cell.attributes.filterable+ '\n' + 'nocache: ' + cell.attributes.nocache :
                    cell.attributes.specimen === 'PIECE' ? 'table: ' + cell.attributes.table + '\n' + 'projection: ' + cell.attributes.projection + '\n' + 'restriction: ' + cell.attributes.restriction + '\n' + 'value: ' + cell.attributes.value :
                    '');
    return r;
};

let mxg_getjson = function (graph) {
    let jsonobject = {};
    try {
        let root = graph.model.cells.root;
        _.each(root.attributes, function(v, k) {
            if (k !== 'specimen' && v !== undefined) {
                jsonobject[k] = JSON.parse(v);
            }
        });
        jsonobject.type = root.attributes.specimen === 'CHART' ? 'gchart' : 'UNKNOWN';
        if (jsonobject.type === 'gchart') {
            jsonobject.yaxis = [];
            _.each(root.edges, function (ye) {
                if (ye.target.attributes.specimen === 'YAXIS') {
                    let yaxis = {};
                    _.each(ye.target.attributes, function(v, k) {
                        if (k !== 'specimen' && v !== undefined) {
                            yaxis[k] = JSON.parse(v);
                        }
                    });
                    yaxis.renderers = [];
                    _.each(ye.target.edges, function(re) {
                        if (re.target.attributes.specimen === 'RENDERER') {
                            let renderer = {};
                            _.each(re.target.attributes, function(v, k) {
                                if (k !== 'specimen' && v !== undefined) {
                                    renderer[k] = JSON.parse(v);
                                }
                            });
                            renderer.datasets = [];
                            _.each(re.target.edges, function(de) {
                                if (de.target.attributes.specimen === 'DATASET') {
                                    let dataset = {};
                                    _.each(de.target.attributes, function(v, k) {
                                        if (k !== 'specimen' && v !== undefined) {
                                            dataset[k] = JSON.parse(v);
                                        }
                                    });
                                    dataset.pieces = [];
                                    _.each(de.target.edges, function(pe) {
                                        if (pe.target.attributes.specimen === 'PIECE') {
                                            let piece = {};
                                            _.each(pe.target.attributes, function(v, k) {
                                                if (k !== 'specimen' && v !== undefined) {
                                                    piece[k] = JSON.parse(v);
                                                }
                                            });
                                            dataset.pieces.push(piece);
                                        }
                                    });
                                    renderer.datasets.push(dataset);
                                }
                            });
                            yaxis.renderers.push(renderer);
                        }
                    });
                    jsonobject.yaxis.push(yaxis);
                }
            });
        }
    }
    catch (err) {
        alertify.error('<div style="font-size:150%;">' + err + "</div>", 20000);
    }
    return jsonobject;
};

let mxg_edit = function (context, container, jsonobject) {
    mxEvent.disableContextMenu(container);
    let graph = new mxGraph(container);
    context.graph = graph;
    graph.attributes = {};
    graph.setCellsMovable(false);
    graph.setCellsResizable(false);
    graph.setCellsEditable(false);
    graph.setAutoSizeCells(true);
    graph.setPanning(true);
    graph.centerZoom = false;
    graph.panningHandler.useLeftButtonForPanning = true;
    graph.panningHandler.popupMenuHandler = false;
    graph.setTooltips(!mxClient.IS_TOUCH);
    graph.popupMenuHandler.factoryMethod = function(menu, cell, evt) {
        return mxg_createPopupMenu(graph, menu, cell, evt);
    };
    let oldGetPreferredSizeForCell = graph.getPreferredSizeForCell;
    graph.getPreferredSizeForCell = function(cell) {
        let result = oldGetPreferredSizeForCell.apply(this, arguments);
        if (result != null) {
            let arr = cell.value.split('\n');
            result.height = _.max([(arr.length + 2 ) * 15, 40]);
            result.width = 9 * _.max(_.map(arr, function (e) {
                return e.length;
            }));
            result.width = _.max([result.width, 400]);
        }
        return result;
    };
    graph.cellRenderer.getTextScale = function(state) {
        return Math.min(1, state.view.scale);
    };
    graph.cellRenderer.getLabelValue = function(state) {
        return state.cell.value;
    };
    graph.addListener(mxEvent.EDITING_STOPPED, mxUtils.bind(this, function() {
        let cell = graph.attributes.current;
        cell.attributes[graph.attributes.edited] = cell.value;
        cell.value = mxg_setValue(cell);
        graph.updateCellSize(cell);    
    }));
    let style = graph.getStylesheet().getDefaultVertexStyle();
    style[mxConstants.STYLE_SHAPE] = 'label';
    style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
    style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_LEFT;
    style[mxConstants.STYLE_STROKECOLOR] = 'black';
    style[mxConstants.STYLE_FILLCOLOR] = 'white';
    style[mxConstants.STYLE_FONTCOLOR] = 'black';
    style[mxConstants.STYLE_FONTFAMILY] = 'Verdana';
    style[mxConstants.STYLE_FONTSIZE] = '12';
    style[mxConstants.STYLE_FONTSTYLE] = '1';
    style[mxConstants.STYLE_SHADOW] = '1';
    style[mxConstants.STYLE_ROUNDED] = '1';
    style[mxConstants.STYLE_GLASS] = '1';
    style[mxConstants.STYLE_SPACING] = 8;
    style = graph.getStylesheet().getDefaultEdgeStyle();
    style[mxConstants.STYLE_ROUNDED] = true;
    style[mxConstants.STYLE_STROKEWIDTH] = 3;
    style[mxConstants.STYLE_EXIT_X] = 0.5; // center
    style[mxConstants.STYLE_EXIT_Y] = 1.0; // bottom
    style[mxConstants.STYLE_EXIT_PERIMETER] = 0; // disabled
    style[mxConstants.STYLE_ENTRY_X] = 0.5; // center
    style[mxConstants.STYLE_ENTRY_Y] = 0; // top
    style[mxConstants.STYLE_ENTRY_PERIMETER] = 0; // disabled
    style[mxConstants.STYLE_EDGE] = mxEdgeStyle.TopToBottom;
    let keyHandler = new mxKeyHandler(graph);
    let layout = new mxCompactTreeLayout(graph, false);
    layout.useBoundingBox = false;
    layout.sortEdges = true;
    layout.edgeRouting = false;
    layout.levelDistance = 60;
    layout.nodeDistance = 16;
    layout.isVertexMovable = function (cell) {
        return true;
    };
    let layoutMgr = new mxLayoutManager(graph);
    layoutMgr.getLayout = function(cell) {
        if (cell.getChildCount() > 0) {
            return layout;
        }
    };
    let parent = graph.getDefaultParent();
    let root;
    graph.getModel().beginUpdate();
    try {
        let w = graph.container.offsetWidth;
        let defx = w/2 - 200;
        let defy = 20;
        let defw = 400;
        let defh = 120;
        if (jsonobject.type === 'gchart') {
            root = graph.insertVertex(parent, 'root', 'CHART', defx, defy, defw, defh, 'fillColor=#E38080');
            root.attributes = {'specimen': 'CHART', 'id': JSON.stringify(jsonobject.id), 'title': JSON.stringify(jsonobject.title), 'subtitle': JSON.stringify(jsonobject.subtitle), 'reftime': JSON.stringify(jsonobject.reftime)};
            root.value = mxg_setValue(root);
            graph.updateCellSize(root);
            mxg_addOverlays(graph, root, true, false, false);
            _.each(jsonobject.yaxis, function (y) {
                let yaxis = graph.insertVertex(parent, null, 'YAXIS', null, null, null, null, 'fillColor=#9E5695');
                yaxis.attributes = {'specimen': 'YAXIS', 'title': JSON.stringify(y.title), 'position': JSON.stringify(y.position), 'scaling': JSON.stringify(y.scaling), 'properties': JSON.stringify(y.properties), 'minvalue': JSON.stringify(y.minvalue), 'maxvalue': JSON.stringify(y.maxvalue)};
                yaxis.value = mxg_setValue(yaxis);
                graph.updateCellSize(yaxis);
                let geometry = graph.getModel().getGeometry(yaxis);
                let size = graph.getPreferredSizeForCell(yaxis);
                geometry.width = size.width;
                geometry.height = size.height;
                let edge = graph.insertEdge(parent, null, '', root, yaxis);
                edge.geometry.x = 1;
                edge.geometry.y = 0;
                edge.geometry.offset = new mxPoint(0, -20);
                mxg_addOverlays(graph, yaxis, true, true, true);
                _.each(y.renderers, function(r) {
                    let renderer = graph.insertVertex(parent, null, 'RENDERER', null, null, null, null, 'fillColor=#EFC161');
                    renderer.attributes = {'specimen': 'RENDERER', 'type': JSON.stringify(r.type)};
                    renderer.value = mxg_setValue(renderer);
                    graph.updateCellSize(renderer);
                    let geometry = graph.getModel().getGeometry(renderer);
                    let size = graph.getPreferredSizeForCell(renderer);
                    geometry.width = size.width;
                    geometry.height = size.height;
                    let edge = graph.insertEdge(parent, null, '', yaxis, renderer);
                    edge.geometry.x = 1;
                    edge.geometry.y = 0;
                    edge.geometry.offset = new mxPoint(0, -20);
                    mxg_addOverlays(graph, renderer, true, true, true);
                    _.each(r.datasets, function(d) {
                        let dataset = graph.insertVertex(parent, null, 'DATASET', null, null, null, null, 'fillColor=#6F92E4');
                        dataset.attributes = {'specimen': 'DATASET', 'groupby': JSON.stringify(d.groupby), 'projection': JSON.stringify(d.projection), 'collections': JSON.stringify(d.collections), 'userfunctions': JSON.stringify(d.userfunctions), 'info': JSON.stringify(d.info), 'onclick': JSON.stringify(d.onclick), 'filterable': JSON.stringify(d.filterable), 'nocache': JSON.stringify(d.nocache)};
                        dataset.value = mxg_setValue(dataset);
                        graph.updateCellSize(dataset);
                        let geometry = graph.getModel().getGeometry(dataset);
                        let size = graph.getPreferredSizeForCell(dataset);
                        geometry.width = size.width;
                        geometry.height = size.height;
                        let edge = graph.insertEdge(parent, null, '', renderer, dataset);
                        edge.geometry.x = 1;
                        edge.geometry.y = 0;
                        edge.geometry.offset = new mxPoint(0, -20);
                        mxg_addOverlays(graph, dataset, true, true, true);
                        _.each(d.pieces, function(p) {
                            let piece = graph.insertVertex(parent, null, 'PIECE', null, null, null, null, 'fillColor=#6AC951');
                            piece.attributes = {'specimen': 'PIECE', 'table': JSON.stringify(p.table), 'projection': JSON.stringify(p.projection), 'restriction': JSON.stringify(p.restriction), 'value': JSON.stringify(p.value)};
                            piece.value = mxg_setValue(piece);
                            graph.updateCellSize(piece);
                            let geometry = graph.getModel().getGeometry(piece);
                            let size = graph.getPreferredSizeForCell(piece);
                            geometry.width = size.width;
                            geometry.height = size.height;
                            let edge = graph.insertEdge(parent, null, '', dataset, piece);
                            edge.geometry.x = 1;
                            edge.geometry.y = 0;
                            edge.geometry.offset = new mxPoint(0, -20);
                            mxg_addOverlays(graph, piece, false, true, true);
                        });
                    });
                });
            });
        }
    }
    finally {
        graph.getModel().endUpdate();
        graph.scrollCellToVisible(root, true);
    }
};

let manage_log = function(url, id, title, file) {
    let ws = new WebSocket(url);
    let uniqueid;
    let data = '';
    ws.onopen = function () {
        uniqueid = _.uniqueId('log');
        let wml = create_window(id, title, undefined, undefined, ws);
        wml.attachHTMLString('<div id="' + uniqueid + '" style="width:100%;height:100%;overflow:auto"></div>');
        ws.send("tail -1000 " + file);
    };
    ws.onmessage = function (e) {
        if (e.data === '__END_OF_PIPE__') {
            ws.close();
        } else {
            data += '<span style="white-space:pre">' + e.data + "</span>";
            setTimeout(function () { document.getElementById(uniqueid).innerHTML=data; }, 50);
        }
    };
    ws.onerror = function (e) {
        alertify.error('<div style="font-size:150%;">' + e.data + "</div>", 20000);
        ws.close();
    };
    ws.onclose = function (e) {
        return;
    };
};

let create_window = function(id, title, w, h, ws) {
    let uid = _.uniqueId(id);
    let width = w === undefined ? desktop.layout.cells("a").getWidth() / 3 * 2 : w;
    let height = h === undefined ? desktop.layout.cells("a").getHeight() / 3 * 2 : h;
    let top = h === undefined ? desktop.layout.cells("a").getHeight() / 6 : (desktop.layout.cells("a").getHeight() - h) / 2;
    let left = w === undefined ? desktop.layout.cells("a").getWidth() / 6 : (desktop.layout.cells("a").getWidth() - w) / 2;
    height = _.min([height, desktop.layout.cells("a").getHeight()]);
    top = height === desktop.layout.cells("a").getHeight() ? 0 : top;
    let win = desktop.windows.createWindow(uid, left, top, width, height);
    win.setText(title);
    desktop.toolbar.addListOption("windows", uid, -1, "button", title);
    win.attachEvent("onParkUp", function () {
        win.hide();
    });
    win.attachEvent("onClose", function () {
        if (ws !== undefined) {
            ws.send("__END_OF_PIPE__");
            ws.close();
        }
        desktop.toolbar.removeListOption("windows", uid);
        return true;
    });
    return win;
};

let login = function (x) {
    let listusers = [];
    _.each(_.sortBy(getallusers(x), function(u) {
        return u.id;
    }), function(u) {
        listusers.push({text: u.id, value: u.value});
    });
    let logindata = [
        {type: "settings", position: "label-left", labelWidth: 200, inputWidth: 200},
        {type: "fieldset", label: "Welcome", inputWidth: 460, list:[
            {type: "select", label: "Login", options: listusers, name: "user"},
            {type: "password", label: "Password", value: "", name: "password"},
            {type: "button", value: "Login", name: "login", width: 400}
        ]},
    ];
    let loginform = desktop.layout.cells("a").attachForm();
    loginform.cross_and_load(logindata, "33%");
    loginform.enableLiveValidation(true);
    loginform.attachEvent("onButtonClick", function(){
        waterfall([
            ajax_post_first_in_async_waterfall("checkuserpassword", {password: loginform.getItemValue("password"), user: loginform.getItemValue("user"), logging: 'fatal'}),
            function (x) {
                log.info(`Connected under ${loginform.getItemValue("user")}!`);
                loginform.cont.style.display = "none";               
                desktop.layout.cells("a").showToolbar();  
                desktop.user = loginform.getItemValue("user");
                desktop.password = loginform.getItemValue("password");
                desktop.adminrights = x.adminrights;
                if (! desktop.adminrights) {
                    desktop.toolbar.disableListOption("kairos", "manage_roles");
                    desktop.toolbar.disableListOption("kairos", "manage_users");
                    desktop.toolbar.disableListOption("kairos", "manage_grants");
                }
                document.title = `KAIROS V${VERSION} / ${desktop.user}`;
                waterfall([
                    ajax_get_first_in_async_waterfall("getsettings", {user: desktop.user}),
                    function (y) {
                        desktop.settings = y.settings;
                    }
                ]);
            }
        ]);
    });
};

let settings = function () {
    let wsettings = create_window("settings", "Settings", 500, 410);
    parallel({
        systemdb: ajax_get_in_async_parallel("listsystemdb"),
        nodesdb: ajax_get_in_async_parallel("listnodesdb", {user: desktop.user}),
        templates: ajax_get_in_async_parallel("listtemplates", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
        wallpapers: ajax_get_in_async_parallel("listwallpapers", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
        colors: ajax_get_in_async_parallel("listcolors", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb})
    }, function (x) {
        let listsystemdb = [];
        _.each(_.sortBy(getallsystemdb(x.systemdb), function(s) {
            return s.id;
        }), function(s) {
            listsystemdb.push({text: s.id, value: s.value, selected: s.value === desktop.settings.systemdb ? true : false});
        });
        let listnodesdb = [];
        _.each(_.sortBy(getallnodesdb(x.nodesdb), function(n) {
            return n.id;
        }), function(n) {
            listnodesdb.push({text: n.id, value: n.value, selected: n.value === desktop.settings.nodesdb ? true : false});
        });
        let listtemplates = [];
        _.each(_.sortBy(getalltemplates(x.templates), function(t) {
            return t.id;
        }), function(t) {
            listtemplates.push({text: t.id, value: t.value, selected: t.value === desktop.settings.template ? true : false});
        });
        let listcolors = [];
        _.each(_.sortBy(getallcolors(x.colors), function(c) {
            return c.id;
        }), function(c) {
            listcolors.push({text: c.id, value: c.value, selected: c.value === desktop.settings.colors ? true : false});
        });
        let listwallpapers = [];
        _.each(_.sortBy(getallwallpapers(x.wallpapers), function(w) {
            return w.id;
        }), function(w) {
            listwallpapers.push({text: w.id, value: w.value, selected: w.value === desktop.settings.wallpaper ? true : false});
        });
        let plotorientation = [];
        _.each(['horizontal', 'vertical'], function (o) {
            plotorientation.push({text: o, value: o, selected: o === desktop.settings.plotorientation ? true : false});
        });
        let listlogging = [];
        _.each(['off', 'fatal', 'error', 'warn', 'info', 'debug', 'trace', 'all'], function (l) {
            listlogging.push({text: l, value: l, selected: l === desktop.settings.logging ? true : false});
        });
        let listtop = [];
        _.each(_.range(1, 101), function (n) {
            listtop.push({text: n, value: n, selected: n === desktop.settings.top ? true : false});
        });

        let settingsdata = [
            {type: "settings", position: "label-left", labelWidth: 200, inputWidth: 200},
            {type: "fieldset", label: "Settings", inputWidth: 460, list:[
                {type: "select", label: "System database", options: listsystemdb, name: "systemdb"},
                {type: "select", label: "Nodes database", options: listnodesdb, name: "nodesdb"},
                {type: "select", label: "Charts template", options: listtemplates, name: "template"},
                {type: "select", label: "Colors definition", options: listcolors, name: "color"},
                {type: "select", label: "Wallpaper", options: listwallpapers, name: "wallpaper"},
                {type: "select", label: "Plot orientation", options: plotorientation, name: "plotorientation"},
                {type: "select", label: "Logging", options: listlogging, name: "logging"},
                {type: "select", label: "Request labels limit", options: listtop, name: "top"},
            ]},
            {type: "button", value: "Update settings", name: "updatesettings", width: 460}
        ];
        let settingsform = wsettings.attachForm();
        settingsform.cross_and_load(settingsdata);
        settingsform.attachEvent("onButtonClick", function(){
            waterfall([
                ajax_get_first_in_async_waterfall("updatesettings", {user: desktop.user, systemdb: settingsform.getItemValue("systemdb"), nodesdb: settingsform.getItemValue("nodesdb"), template: settingsform.getItemValue("template"), colors: settingsform.getItemValue("color"), wallpaper: settingsform.getItemValue("wallpaper"), top: settingsform.getItemValue("top"), plotorientation: settingsform.getItemValue("plotorientation"), logging: settingsform.getItemValue("logging")}),
                function (x) {
                    waterfall([
                        ajax_get_first_in_async_waterfall("getsettings", {user: desktop.user}),
                        function (y) {
                            desktop.settings = y.settings;
                            wsettings.close();
                        }
                    ]);
                }
            ]);
        });
    });
};


let edit_object = function (out, mog, currow, nid) {
    let objid = null;
    let objtype = null;
    let objdatabase = null;
    if (out) {
        objid = mog;
        objdatabase = currow;
        objtype = "liveobject";
    } else {
        objid = mog.cellById(currow, 1).getValue();
        objtype = mog.cellById(currow, 2).getValue();
        objdatabase = mog.cellById(currow,4).getValue();
    }
    let weo = create_window("edit_object", "Edit object - " + objtype + " : " + objid);
    let wet = weo.attachToolbar({});
    let toolbardata = [
        {type: "button", id: "save", text: "Save", title: "Save"},
    ];
    wet.loadStruct(toolbardata);
    wet.attachEvent("onClick", function(id){
        if (id === "save") {
            save_object();
        }
    });
    let oid = _.uniqueId('edit');
    weo.attachHTMLString('<pre id="' + oid + '" style="margin:0;position:relative;top:0,bottom:0;right:0;left:0;"></pre>');
    let editor = ace.edit(oid);
    editor.getSession().setMode("ace/mode/python");
    editor.setKeyboardHandler("ace/keyboard/vim");
    editor.$blockScrolling = Infinity;
    document.getElementById(oid).style.height = weo.cell.childNodes[1].clientHeight;
    weo.attachEvent("onResizeFinish", function () {
        document.getElementById(oid).style.height = weo.cell.childNodes[1].clientHeight;
        editor.resize();
    });
    weo.attachEvent("onMaximize", function () {
        document.getElementById(oid).style.height = weo.cell.childNodes[1].clientHeight;
        editor.resize();
    });
    weo.attachEvent("onMinimize", function () {
        document.getElementById(oid).style.height = weo.cell.childNodes[1].clientHeight;
        editor.resize();
    });
    let save_object = function () {
        waterfall([
            ajax_post_first_in_async_waterfall("setobject", {database: objdatabase, source: editor.getValue(), encoded: 0}),
            function (x) {
                if (out) {
                    waterfall([
                        ajax_get_first_in_async_waterfall("applyliveobject", {nodesdb: objdatabase, systemdb: desktop.settings.systemdb, id: nid, liveobject: x.id}),
                        function (x) {
                        }
                    ]);
                } else {
                    waterfall([
                        ajax_get_first_in_async_waterfall("listobjects", {systemdb: desktop.settings.systemdb, nodesdb: objdatabase}),
                        function (x) {
                            let datarows = [];
                            _.each(_.sortBy(getallobjects(x), function(o) {
                                return o.id;
                            }), function(o) {
                                datarows.push({id: o.id, data: [o.id, o.name, o.type, o.created, o.origin]});
                            });
                            mog.clearAll();
                            mog.parse({rows: datarows}, "json");
                            
                        }
                    ]);
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                }
            }
        ]);
    };
    waterfall([
        ajax_get_first_in_async_waterfall("getobject", {database: objdatabase, id: objid, type: objtype}),
        function (x) {
            editor.setValue(x); 
        }
    ]);
};

let manage_objects = function () {
    let wmo = create_window("manage_objects", "Manage objects");
    let mog = wmo.attachGrid();
    mog.setHeader("Id,Object,Type,Created,Origin");
    mog.setColSorting("str,str,str,str,str");
    mog.attachHeader("#text_filter,#text_filter,#text_filter,#text_filter,#text_filter");
    mog.init();
    mog.enableSmartRendering(true);
    let mot = wmo.attachToolbar({});
    let currow = null;
    mog.attachEvent("onRowSelect", function(id){
        currow = id;
        mot.enableItem("download_object");
        mot.enableItem("delete_object");
        mot.enableItem("edit_object");
        if (_.contains(['gchart', 'gdataset'], mog.cellById(currow, 2).getValue())) {
            mot.enableItem("graphical_edit_object");
        } else {
            mot.disableItem("graphical_edit_object");
        }
    });
    let upload_object = function () {
        upload(makeURL("uploadobject", {nodesdb: desktop.settings.nodesdb}), refresh);
    };
    let download_object = function () {
        window.location.href = '/downloadobject?id=' + mog.cellById(currow, 1).getValue() + '&type=' + mog.cellById(currow, 2).getValue() + '&database=' + mog.cellById(currow,4).getValue();
    };
    let delete_object = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("deleteobject", {id : mog.cellById(currow, 1).getValue(), type: mog.cellById(currow, 2).getValue(), database: mog.cellById(currow,4).getValue()}),
            function (x) {
                alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                mog.deleteRow(currow);
                mot.disableItem("download_object");
                mot.disableItem("delete_object");
                mot.disableItem("edit_object");
                mot.disableItem("graphical_edit_object");
            }
        ]);
    };
    let graphical_edit_object = function () {
        let objid = mog.cellById(currow, 1).getValue();
        let objtype = mog.cellById(currow, 2).getValue();
        let objdatabase = mog.cellById(currow,4).getValue();
        let context = {};
        let wgeo = create_window("graphical_edit_object", "Graphical Edit - " + objtype + " : " + objid);
        let wget = wgeo.attachToolbar({});
        let toolbardata = [
            {type: "button", id: "save", text: "Save", title: "Save"},
            {type: "button", id: "generate", text: "Generate", title: "Generate"},
        ];
        wget.loadStruct(toolbardata);
        wget.attachEvent("onClick", function(id){
            if (id === "save") {
                save_object();
            }
            if (id === "generate") {
                generate_object();
            }
        });
        let uniquecid = _.uniqueId('graphedit');
        wgeo.attachHTMLString('<div id="' + uniquecid + '" style="width:100%;height:100%;overflow:auto"></div>');
        let container = document.getElementById(uniquecid);
        let save_object = function () {
            let jsongraph = mxg_getjson(context.graph);
            let source = '\nobject = ' + JSON.stringify(jsongraph, undefined, 4) + '\nsuper(UserObject, s).__init__(**object)';
            source = '\ndef __init__(s):' + source.replace(/\n/g, '\n    ');
            source = 'null=None\ntrue=True\nfalse=False\n\nclass UserObject(dict):' + source.replace(/\n/g, '\n    ');
            waterfall([
                ajax_post_first_in_async_waterfall("setobject", {database: desktop.settings.nodesdb, source: source, encoded: 0}),
                function (x) {
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    refresh();
                }
            ]);
        };
        let generate_object = function() {
            let jsongraph = mxg_getjson(context.graph);
            let clonegraph = JSON.parse(JSON.stringify(jsongraph));
            let chartid = jsongraph.id;
            let queries = {};
            let i = 0;
            _.each(jsongraph.yaxis, function (y, iy) {
                _.each(y.renderers, function (r, ir) {
                    _.each(r.datasets, function (d, id) {
                        i += 1;
                        queries[i] = d;
                        clonegraph.yaxis[iy].renderers[ir].datasets[id] = {query: chartid + "$$" + i, timestamp: "timestamp", label: "label", value: "value", info: d.info === null ? undefined : d.info, onclick: d.onclick === null ? undefined : d.onclick};
                    });
                });
            });
            _.each(queries, function(q, i) {
                let pieces = [];
                _.each(q.pieces, function(p) {
                    let where = p.restriction === undefined || p.restriction === null || p.restriction === "" ? "" : " where " + p.restriction;
                    pieces.push("select timestamp, " + p.projection + " as label, " + p.value + " as value from " + p.table + where);
                });
                let query = {type: "query", id: chartid + '$$' + i, collections: q.collections, userfunctions: q.userfunctions, request: "select timestamp, " + q.projection + " as label, " + q.groupby + "(value) as value from (" + pieces.join(" union all ") + ") as foo group by timestamp, label order by timestamp", nocache: q.nocache === undefined ? false : q.nocache, filterable: q.filterable === undefined ? true : q.filterable};
                let source = '\nobject = ' + JSON.stringify(query, undefined, 4) + '\nsuper(UserObject, s).__init__(**object)';
                source = '\ndef __init__(s):' + source.replace(/\n/g, '\n    ');
                source = 'class UserObject(dict):' + source.replace(/\n/g, '\n    ');
                waterfall([
                    ajax_post_first_in_async_waterfall("setobject", {database: desktop.settings.nodesdb, source: source, encoded: 0}),
                    function (x) {
                        alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    }
                ]);
            });
            clonegraph.type = "chart";
            let source = '\nobject = ' + JSON.stringify(clonegraph, undefined, 4) + '\nsuper(UserObject, s).__init__(**object)';
            source = '\ndef __init__(s):' + source.replace(/\n/g, '\n    ');
            source = 'class UserObject(dict):' + source.replace(/\n/g, '\n    ');
            waterfall([
                ajax_post_first_in_async_waterfall("setobject", {database: desktop.settings.nodesdb, source: source, encoded: 0}),
                function (x) {
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    refresh();
                }
            ]);
        };
        waterfall([
            ajax_get_first_in_async_waterfall("getjsonobject", {database: objdatabase, id: objid, type: objtype}),
            function (x) {
                mxg_edit(context, container, x);
            }
        ]);
    };

    let toolbardata = [
        {type: "button", id: "upload_object", text: "Upload object", title: "Upload object"},
        {type: "separator"},
        {type: "button", id: "download_object", text: "Download object", title: "Download object", enabled: false},
        {type: "separator"},
        {type: "button", id: "delete_object", text: "Delete object", title: "Delete object", enabled: false},
        {type: "separator"},
        {type: "button", id: "edit_object", text: "Edit object", title: "Edit object", enabled: false},
        {type: "separator"},
        {type: "button", id: "graphical_edit_object", text: "Graphical Edit", title: "Graphical Edit", enabled: false},
    ];
    mot.loadStruct(toolbardata);
    mot.attachEvent("onClick", function(id){
        if (id === "upload_object") {
            upload_object();
        }
        if (id === "download_object") {
            download_object();
        }
        if (id === "delete_object") {
            delete_object();
        }
        if (id === "edit_object") {
            edit_object(false, mog, currow);
        }
        if (id === "graphical_edit_object") {
            graphical_edit_object();
        }
    });

    let refresh = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("listobjects", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
            function (x) {
                let datarows = [];
                _.each(_.sortBy(getallobjects(x), function(o) {
                    return o.id;
                }), function(o) {
                    datarows.push({id: o.id, data: [o.id, o.name, o.type, o.created, o.origin]});
                });
                mog.clearAll();
                mog.parse({rows: datarows}, "json");
            }
        ]);
    };

    refresh();

};

let manage_roles = function () {
    let wmr = create_window("manage_roles", "Manage roles");
    let mrg = wmr.attachGrid();
    mrg.setHeader("Rid,Role");
    mrg.setColSorting("str,str");
    mrg.attachHeader("#text_filter,#text_filter");
    mrg.init();
    mrg.enableSmartRendering(true);
    let mrt = wmr.attachToolbar({});
    let currow = null;
    mrg.attachEvent("onRowSelect", function(id){
        currow = id;
        mrt.enableItem("delete_role");
    });
    let create_role = function () {
        let wcr = create_window("crrole", "Create role", 540, 160);
        let data = [
            {type: "settings", position: "label-left", labelWidth: 100, inputWidth: 300},
            {type: "fieldset", label: "Create role", inputWidth: 460, list:[
                {type: "input", label: "Role", name: "role"},
            ]},
            {type: "button", value: "Create", name: "createrole", width: 460}
        ];
        let crf = wcr.attachForm();
        crf.cross_and_load(data);
        crf.attachEvent("onButtonClick", function() {
            waterfall([
                ajax_get_first_in_async_waterfall("createrole", {role: crf.getItemValue("role")}),
                function (x) {
                    wcr.close();
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    refresh();
                }
            ]);
        });
    };
    let delete_role = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("deleterole", {role : mrg.cellById(currow, 0).getValue()}),
            function (x) {
                alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                mrg.deleteRow(currow);
                mrt.disableItem("delete_role");
            }
        ]);
    };

    let toolbardata = [
        {type: "button", id: "create_role", text: "Create role", title: "Create role"},
        {type: "separator"},
        {type: "button", id: "delete_role", text: "Delete role", title: "Delete role", enabled: false},
    ];
    mrt.loadStruct(toolbardata);
    mrt.attachEvent("onClick", function(id){
        if (id === "create_role") {
            create_role();
        }
        if (id === "delete_role") {
            delete_role();
        }
    });

    let refresh = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("listroles"),
            function (x) {
                let datarows = [];
                _.each(_.sortBy(getallroles(x), function(r) {
                    return r.id;
                }), function(r) {
                    datarows.push({id: r.id, data: [r.id, r.value]});
                });
                mrg.clearAll();
                mrg.parse({rows: datarows}, "json");
            }
        ]);
    };

    refresh();

};

let manage_users = function () {
    let wmu = create_window("manage_users", "Manage users");
    let mug = wmu.attachGrid();
    mug.setHeader("Uid,User");
    mug.setColSorting("str,str");
    mug.attachHeader("#text_filter,#text_filter");
    mug.init();
    mug.enableSmartRendering(true);
    let mut = wmu.attachToolbar({});
    let currow = null;
    mug.attachEvent("onRowSelect", function(id){
        currow = id;
        mut.enableItem("delete_user");
        mut.enableItem("reset_password");
    });
    let create_user = function () {
        let wcu = create_window("cruser", "Create user", 540, 160);
        let data = [
            {type: "settings", position: "label-left", labelWidth: 100, inputWidth: 300},
            {type: "fieldset", label: "Create user", inputWidth: 460, list:[
                {type: "input", label: "User", name: "user"},
            ]},
            {type: "button", value: "Create", name: "createuser", width: 460}
        ];
        let crf = wcu.attachForm();
        crf.cross_and_load(data);
        crf.attachEvent("onButtonClick", function() {
            waterfall([
                ajax_get_first_in_async_waterfall("createuser", {user: crf.getItemValue("user")}),
                function (x) {
                    wcu.close();
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    refresh();
                }
            ]);
        });
    };
    let delete_user = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("deleteuser", {user : mug.cellById(currow, 0).getValue()}),
            function (x) {
                alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                mug.deleteRow(currow);
                mut.disableItem("delete_user");
                mut.disableItem("reset_password");
            }
        ]);
    };
    let reset_password = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("resetpassword", {user : mug.cellById(currow, 0).getValue()}),
            function (x) {
                alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
            }
        ]);
    };

    let toolbardata = [
        {type: "button", id: "create_user", text: "Create user", title: "Create user"},
        {type: "separator"},
        {type: "button", id: "delete_user", text: "Delete user", title: "Delete user", enabled: false},
        {type: "separator"},
        {type: "button", id: "reset_password", text: "Reset password", title: "Reset password", enabled: false},
    ];
    mut.loadStruct(toolbardata);
    mut.attachEvent("onClick", function(id){
        if (id === "create_user") {
            create_user();
        }
        if (id === "delete_user") {
            delete_user();
        }
        if (id === "reset_password") {
            reset_password();
        }
    });

    let refresh = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("listusers"),
            function (x) {
                let datarows = [];
                _.each(_.sortBy(getallusers(x), function(r) {
                    return r.id;
                }), function(r) {
                    datarows.push({id: r.id, data: [r.id, r.value]});
                });
                mug.clearAll();
                mug.parse({rows: datarows}, "json");
            }
        ]);
    };

    refresh();
};

let manage_grants = function () {
    let wmg = create_window("manage_grants", "Manage grants", 540, 200);
    let mgg = wmg.attachGrid();
    mgg.setHeader("Gid,user,role");
    mgg.setColSorting("str,str,str");
    mgg.attachHeader("#text_filter,#text_filter,#text_filter");
    mgg.init();
    mgg.enableSmartRendering(true);
    let mgt = wmg.attachToolbar({});
    let currow = null;
    mgg.attachEvent("onRowSelect", function(id){
        currow = id;
        mgt.enableItem("revoke_role");
    });
    let grant_role = function () {
        let wcg = create_window("crgrant", "Grant role", 540, 200);
        let data = [
            {type: "settings", position: "label-left", labelWidth: 100, inputWidth: 300},
            {type: "fieldset", label: "Grant role to user", inputWidth: 460, list:[
                {type: "input", label: "User", name: "user"},
                {type: "input", label: "Role", name: "role"},
            ]},
            {type: "button", value: "Grant", name: "grant", width: 460}
        ];
        let crf = wcg.attachForm();
        crf.cross_and_load(data);
        crf.attachEvent("onButtonClick", function() {
            waterfall([
                ajax_get_first_in_async_waterfall("creategrant", {user: crf.getItemValue("user"), role: crf.getItemValue("role")}),
                function (x) {
                    wcg.close();
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    refresh();
                }
            ]);
        });
    };
    let revoke_role = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("deletegrant", {user : mgg.cellById(currow, 1).getValue(), role: mgg.cellById(currow, 2).getValue()}),
            function (x) {
                alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                mgg.deleteRow(currow);
                mgt.disableItem("revoke_role");
            }
        ]);
    };

    let toolbardata = [
        {type: "button", id: "grant_role", text: "Grant role", title: "Grant role"},
        {type: "separator"},
        {type: "button", id: "revoke_role", text: "Revoke role", title: "Revoke role", enabled: false},
    ];
    mgt.loadStruct(toolbardata);
    mgt.attachEvent("onClick", function(id){
        if (id === "grant_role") {
            grant_role();
        }
        if (id === "revoke_role") {
            revoke_role();
        }
    });

    let refresh = function () {
        waterfall([
            ajax_get_first_in_async_waterfall("listgrants"),
            function (x) {
                let datarows = [];
                _.each(_.sortBy(getallgrants(x), function(g) {
                    return g.id;
                }), function(g) {
                    datarows.push({id: g.id, data: [g.id, g.user, g.role]});
                });
                mgg.clearAll();
                mgg.parse({rows: datarows}, "json");
            }
        ]);
    };
    refresh();
};

let manage_password = function () {
    let wpassword = create_window("manage_password", "Manage password", 500, 230);
    let passworddata = [
        {type: "settings", position: "label-left", labelWidth: 140, inputWidth: 260},
        {type: "fieldset", label: "Manage password", inputWidth: 460, list:[
            {type: "password", label: "Actual password", value: "", name: "actual"},
            {type: "password", label: "New password", value: "", name: "new"},
            {type: "password", label: "Repeat new password", value: "", name: "repeat"},
        ]},
        {type: "button", value: "Set new password", name: "setpassword", width: 460}
    ];
    let passwordform = wpassword.attachForm();
    passwordform.cross_and_load(passworddata);
    passwordform.attachEvent("onButtonClick", function(){
        if (passwordform.getItemValue("new") !== passwordform.getItemValue("repeat")) {
            alertify.error('<div style="font-size:150%;">' + "New and repeated passwords are not identicals !" + "</div>", 20000);
        } else {
            waterfall([
                ajax_post_first_in_async_waterfall("changepassword", {user: desktop.user, password: passwordform.getItemValue("actual"), new: passwordform.getItemValue("new"), logging: 'fatal'}),
                function (x) {
                    alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    desktop.password = passwordform.getItemValue("new");
                    wpassword.close();
                }
            ]);
        }
    });
};

let kairos_log = function () {
    let prefix = "wss://" + window.location.host;
    manage_log(prefix + "/get_kairos_log", "kairos_log", "KAIROS log", "/var/log/kairos/kairos.log");
};

let postgres_logfile = function () {
    let prefix = "wss://" + window.location.host;
    manage_log(prefix + "/get_postgres_logfile", "postgres_logfile", "PostgreSQL log", "/var/lib/pgsql/data/$(cut -f 2 -d ' ' /var/lib/pgsql/data/current_logfiles)");
};

let webserver_log = function () {
    let prefix = "wss://" + window.location.host;
    manage_log(prefix + "/get_webserver_log", "webserver_log", "WEBSERVER log", "/var/log/kairos/webserver.log");
};

let documentation = function () {
    window.location.href = 'https://openkairos.freshdesk.com/solution/categories';
};

let list_databases = function () {
    let wld = create_window("list_databases", "List databases");
    let ldg = wld.attachGrid();
    ldg.setHeader("Database,Size on disk (GB)");
    ldg.setColTypes("ro,ron"); 
    ldg.setColSorting("str,int");
    ldg.init();
    ldg.enableSmartRendering(true);
    waterfall([
        ajax_get_first_in_async_waterfall("listdatabases", {user: desktop.user, admin: desktop.adminrights}),
        function (x) {
            let datarows = [];
            _.each(_.sortBy(getalldatabases(x), function(d) {
                return d.id;
            }), function(d) {
                datarows.push({id: d.id, data: [d.id, d.size]});
            });
            ldg.parse({rows: datarows}, "json");
        }
    ]);
};

let manage_node = function (tree, id, nodeorigin) {
    let node = nodeorigin;
    let gendataform = function (w, listaggregators, listliveobjects, uid1, uid2) {
        let width = w.cont.clientWidth;
        let sizeunit = (width - 132) / 9;
        let type = node.datasource.type;
        
        let generalproperties = [];
        generalproperties.push({
            type: "block",
            list: [
                {type: "input", label: "Type", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 2, value: type, readonly: true},
                {type: "newcolumn"},
                {type: "calendar", dateFormat: "%Y-%m-%d %H:%i", label: "Created", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 2, value: node.created, enableTime: true, readonly: true, calendarPosition: "right"},
                {type: "newcolumn"},
                {type: "input", label: "Status", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 2, value: node.status, readonly: true}
            ]
        });
        if (_.contains(["B"], type)) {
            generalproperties.push({
                type: "block",
                list: [
                    {type: "calendar", dateFormat: "%Y-%m-%d %H:%i", label: "Uploaded", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 8, value: node.datasource.uploaded, enableTime: true, readonly: true, calendarPosition: "right"},
                ]
            });
        }
        let general = {type: "fieldset", label: "General properties", list: generalproperties};

        let aggregatorproperties = [];
        aggregatorproperties.push({
            type: "block",
            list: [
                {type: "input", label: "Selector", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 8, name: "aggregatorselector", value: type === 'N' ? '/' : node.datasource.aggregatorselector}
            ]
        });
        aggregatorproperties.push({
            type: "block",
            list: [
                {type: "input", label: "Take", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 2, name: "aggregatortake", value: type === 'N' ? 1 : node.datasource.aggregatortake},
                {type: "newcolumn"},
                {type: "input", label: "Skip", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 2, name: "aggregatorskip", value: type === 'N' ? 0 : node.datasource.aggregatorskip},
                {type: "newcolumn"},
                {type: "select", label: "Sort", labelAlign: "right", labelWidth: sizeunit, name: "aggregatorsort", inputWidth: sizeunit * 2, options: [
                    {text: 'asc', selected: type === 'N' ? false : node.datasource.aggregatorsort === 'asc' ? true : false},
                    {text: 'desc', selected: type === 'N' ? true : node.datasource.aggregatorsort === 'desc' ? true : false},
                ]}
            ]
        });
        aggregatorproperties.push({
            type: "block",
            list: [
                {type: "input", label: "TimeFilter", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 8, name: "aggregatortimefilter", value: type === 'N' ? '.' : node.datasource.aggregatortimefilter}
            ]
        });
        aggregatorproperties.push({
            type: "block",
            list: [
                {type: "select", label: "Method", labelAlign: "right", labelWidth: sizeunit, name: "aggregatormethod", inputWidth: sizeunit * 2, options: listaggregators, value: type === "N" ? '$none' : node.datasource.aggregatormethod},
                {type: "newcolumn"},
                {type: "calendar", dateFormat: "%Y-%m-%d %H:%i", label: "Aggregated", labelAlign: "right", labelWidth: sizeunit, inputWidth: sizeunit * 2, value: type === "N" ? '' : node.datasource.aggregated, enableTime: true, readonly: true, calendarPosition: "right"},
                {type: "newcolumn"},
                {type: "button", width: sizeunit * 3, value: "Apply aggregator", name: "aggregate"}
            ]
        });
      
        let aggregator = {type: "fieldset", label: "Aggregator", list: aggregatorproperties};

        let livenodeproperties = [];
        livenodeproperties.push({
            type: "block",
            list: [
                {type: "select", label: "Live object", labelAlign: "right", labelWidth: sizeunit, name: "liveobject", inputWidth: sizeunit * 7 / 2, options: listliveobjects},
                {type: "newcolumn"},
                {type: "button", width: sizeunit * 9 / 2, value: "Apply live object", name: "makelive"}
            ]
        });

        let livenode = {type: "fieldset", label: "Live node", list: livenodeproperties};

        let producersproperties = [];
        producersproperties.push({
            type: "block",
            list: [
                {type: "container", name: uid1, inputWidth: sizeunit * 9, inputHeight: 300},
            ]
        });

        let producers = {type: "fieldset", label: "Producers", list: producersproperties};

        let collectionsproperties = [];
        collectionsproperties.push({
            type: "block",
            list: [
                {type: "container", name : uid2, inputWidth: sizeunit * 9, inputHeight: 300},
            ]
        });
        collectionsproperties.push({
            type: "block",
            list: [
                {type: "button", width: sizeunit * 9 / 4, value: "Build all caches", name: "buildall"},
                {type: "newcolumn"},
                {type: "button", width: sizeunit * 9 / 4, value: "Build collection cache", name: "buildcolcache", disabled: true},
                {type: "newcolumn"},
                {type: "button", width: sizeunit * 9 / 4, value: "Drop collection cache", name: "dropcolcache", disabled: true},
                {type: "newcolumn"},
                {type: "button", width: sizeunit * 9 / 4, value: "Clear collections caches", name: "clearall"}
            ]
        });

        let collections = {type: "fieldset", label: "Collections", list: collectionsproperties};

        let nodeproperties = [general];
        if (_.contains(["A", "L", "N"], type)) {
            nodeproperties.push(aggregator);
        }
        if (_.contains(["D", "N"], type)) {
            nodeproperties.push(livenode);
        }
        if (_.contains(["A", "C", "L"], type)) {
            nodeproperties.push(producers);
        }
        if (_.contains(["A", "B"], type)) {
            nodeproperties.push(collections);
        }
        let data = [
            {type: "fieldset", label: "Node properties", list: nodeproperties, name: "node_properties"}
        ];
        return data;
    };
    let genform = function (w, listaggregators, listliveobjects) {
        let wf = w.attachForm();

        let uid1= _.uniqueId('grid');
        let uid2= _.uniqueId('grid');
        let curcollection = null;
        wf.cross_and_load(gendataform(wf, listaggregators, listliveobjects, uid1, uid2));

        let gp = new dhtmlXGridObject(wf.getContainer(uid1));
        gp.setHeader("Node path, Node id");
        gp.setColSorting("str,str");
        gp.attachHeader("#text_filter,#text_filter");
        gp.init();
        gp.enableSmartRendering(true);
        let gprows = [];
        _.each(node.datasource.producers, function(r) {
            gprows.push({id: r.id, data: [r.path, r.id]});
        });
        gp.clearAll();
        gp.parse({rows: gprows}, "json");

        let gc = new dhtmlXGridObject(wf.getContainer(uid2));
        gc.setHeader("Id,Collection,Partition,Analyzer,Cache creation date");
        gc.setColSorting("str,str,str,str,str");
        gc.attachHeader("#text_filter,#text_filter,#text_filter,#text_filter,#text_filter");
        gc.init();
        gc.enableSmartRendering(true);
        let gcrows = [];
        _.each(getcollections(node), function(r) {
            gcrows.push({id: r.id, data: [r.id, r.collection, r.partition, r.analyzer, r.created]});
        });
        gc.clearAll();
        gc.parse({rows: gcrows}, "json");
        gc.attachEvent("onRowSelect", function(id){
            curcollection = gc.cells(id, 1).getValue();
            wf.enableItem("buildcolcache");
            wf.enableItem("dropcolcache");
        });
        wf.attachEvent("onButtonClick", function (btn) {
            let f = function(method, params) {
                waterfall([
                    ajax_get_first_in_async_waterfall(method, params),
                    function () {
                        waterfall([
                            ajax_get_first_in_async_waterfall("getnode", {nodesdb: desktop.settings.nodesdb, id: id}),
                            function (x) {
                                node = x;
                                genform(w, listaggregators, listliveobjects);
                                tree.unselectItem(id);
                                tree.selectItem(id);
                                let pid = tree.getParentId(id);
                                tree.refreshItem(pid);
                            }
                        ]);
                    }
                ]);                   
            };
            if (btn === 'buildall') {
                f("buildallcollectioncaches", {nodesdb: desktop.settings.nodesdb, id: id, systemdb: desktop.settings.systemdb});
            }
            if (btn === 'buildcolcache') {
                f("buildcollectioncache", {nodesdb: desktop.settings.nodesdb, id: id, systemdb: desktop.settings.systemdb, collection: curcollection});
            }
            if (btn === 'dropcolcache') {
                f("dropcollectioncache", {nodesdb: desktop.settings.nodesdb, id: id, systemdb: desktop.settings.systemdb, collection: curcollection});
            }
            if (btn === 'clearall') {
                f("clearcollectioncache", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id});
            }
            if (btn === 'aggregate') {
                f("applyaggregator", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id, aggregatorselector: wf.getItemValue("aggregatorselector"), aggregatortake: wf.getItemValue("aggregatortake"), aggregatortimefilter: wf.getItemValue("aggregatortimefilter"), aggregatorskip: wf.getItemValue("aggregatorskip"), aggregatorsort: wf.getItemValue("aggregatorsort"), aggregatormethod: wf.getItemValue("aggregatormethod")});
            }
            if (btn === 'makelive') {
                f("applyliveobject", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id, liveobject: wf.getItemValue("liveobject")});
            }
        });
        return wf;
    };
    parallel({
        aggregators: ajax_get_in_async_parallel("listaggregators", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
        liveobjects: ajax_get_in_async_parallel("listliveobjects", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb})
    }, function (x) {
        let listaggregators = [];
        _.each(_.sortBy(x.aggregators, function(a) {
            return a.id;
        }), function(a) {
            listaggregators.push({text: a.id, value: a.id, selected: node.datasource.type === "N" ? a.id === "$none" ? true : false : a.id === node.datasource.aggregatormethod ? true : false});
        });
        let listliveobjects = [{text: "", value:""}];
        _.each(_.sortBy(x.liveobjects, function(l) {
            return l.id;
        }), function(l) {
            listliveobjects.push({text: l.id, value: l.id, selected: node.datasource.type === "N" ? l.id === undefined ? true : false : l.id === node.datasource.liveobject ? true : false});
        });
        let h = node.datasource.type === "A" ? 1120 : node.datasource.type === "B" ? 610 : node.datasource.type === "C" ? 540 : node.datasource.type === "D" ? 260 : node.datasource.type === "N" ? 450 : node.datasource.type === "T" ? 175 : undefined;
        let wn = create_window("manage_node", desktop.settings.nodesdb + ':' + tree.getPath(id), undefined, h);
        let wf = genform(wn, listaggregators, listliveobjects);
        wn.attachEvent("onResizeFinish", function () {
            wf = genform(wn, listaggregators, listliveobjects);
        });
        wn.attachEvent("onMaximize", function () {
            wf = genform(wn, listaggregators, listliveobjects);
        });
        wn.attachEvent("onMinimize", function () {
            wf = genform(wn, listaggregators, listliveobjects);
        });
    });
};

let upload = function (url, onClose) {
    let wu = create_window("upload", "Upload ...");
    wu.attachEvent("onClose", function() {
        onClose();
        return true;
    });
    let vault = wu.attachVault({
        uploadUrl:  url
    });
};

let rename = function (oldname, callback) {
    let wr = create_window("rename", "Rename ...", 500, 145);
    let data = [
        {type: "settings", label: "", position: "label-left", labelWidth: 200, inputWidth: 200},
        {type: "fieldset", inputWidth: 460, list:[
            {type: "input", label: "Rename to ...",  name: "new", value: oldname},
        ]},
        {type: "button", value: "Rename", name: "rename", width: 460}
    ];
    let wf = wr.attachForm();
    wf.cross_and_load(data);
    wf.attachEvent("onButtonClick", function(){
        let newname = wf.getItemValue("new");
        wr.close();
        callback(newname);
    });
};

let getchoice = function (listchoices, callback) {
    let wgc = create_window("get_choice", "Choose ...", 500, 145);
    let data = [
        {type: "settings", label: "", position: "label-left", labelWidth: 150, inputWidth: 250},
        {type: "fieldset", inputWidth: 460, list:[
            {type: "combo", label: "Choose", options: listchoices, name: "choice"},
        ]},
        {type: "button", value: "Choose", name: "choose", width: 460}
    ];
    let wf = wgc.attachForm();
    wf.cross_and_load(data);
    let cb = wf.getCombo("choice");
    cb.enableFilteringMode(true);
    cb.unSelectOption();
    wf.attachEvent("onButtonClick", function(){
        let choice = wf.getItemValue("choice");
        wgc.close();
        callback(choice);
    });
};


let explorer = function () {
    let wexp = create_window("explorer", desktop.settings.nodesdb);
    let onclick = null;
    let curnode = null;
    let rootid = null;
    let trashid = null;
    let startpid = null;
    let xid = null;
    let yid = null;
    let potentialmenus = null;
    let menu = wexp.attachMenu({
        iconset: "awesome"
    });
    menu.setOpenMode("win");
    let tree = wexp.attachTreeView({
        dnd: true,
        multiselect: true,
        context_menu: true,
        json: "gettree?nodesdb=" + desktop.settings.nodesdb + "&id={id}"
    });
    tree.attachEvent("onContextMenu", function(id, x, y, ev){
        return false;
    });
    tree.attachEvent("onBeforeDrag", function (id) {
        startpid = tree.getParentId(id);
        if (tree.getUserData(id, "type") === "T" || tree.getItemText(id) === '/') {
            return false;
        } else {
            return true;
        }
    });
    tree.attachEvent("onBeforeDrop", function (id, pid) {
        let ret = true;
        if (desktop.mouseevent.ctrlKey === false && desktop.mouseevent.shiftKey === false && desktop.mouseevent.altKey === false && desktop.mouseevent.metaKey === false && pid !== startpid) {
            if (tree.getUserData(pid, "type") !== "T") {
                _.each(tree.getSubItems(pid), function (e) {
                    if (tree.getItemText(id) === tree.getItemText(e)) {
                        alertify.error('<div style="font-size:150%;">' + "A child of '" + tree.getItemText(pid) + "' has already the name: '" + tree.getItemText(e) + "'" + "</div>", 20000);
                        ret = false;
                    }
                });
            }
        }
        if (desktop.mouseevent.altKey) {
            if (_.contains(["C", "L", "N", "T"], tree.getUserData(id, "type"))) {
                ret = false;
            }
            if (_.contains(["B", "C", "D", "L", "T"], tree.getUserData(pid, "type"))) {
                ret = false;
            }
            xid = tree.getParentId(id);
            yid = tree.getParentId(pid);
        }
        if (desktop.mouseevent.ctrlKey  || desktop.mouseevent.shiftKey) {
            if (_.contains(["C", "L", "N", "T"], tree.getUserData(id, "type"))) {
                ret = false;
            }
            if (_.contains(["A", "B", "D", "L", "T"], tree.getUserData(pid, "type"))) {
                ret = false;
            }
            xid = tree.getParentId(id);
            yid = tree.getParentId(pid);
        }
        if (desktop.mouseevent.metaKey) {
            if (_.contains(["A", "B", "C", "D", "L", "T"], tree.getUserData(id, "type"))) {
                ret = false;
            }
            if (_.contains(["A", "B", "C", "D", "T"], tree.getUserData(pid, "type"))) {
                ret = false;
            }
            xid = tree.getParentId(id);
            yid = tree.getParentId(pid);
        }
        return ret;
    });
    tree.attachEvent("onDrop", function (id, pid) {

        if (desktop.mouseevent.ctrlKey === false && desktop.mouseevent.shiftKey === false && desktop.mouseevent.altKey === false && desktop.mouseevent.metaKey === false && pid !== startpid) {
            waterfall([
                ajax_get_first_in_async_waterfall("movenode", {nodesdb: desktop.settings.nodesdb, from: id, to: pid}),
                function () {
                }
            ]);
        }
        if (desktop.mouseevent.altKey) {
            waterfall([
                ajax_get_first_in_async_waterfall("aggregateaddnode", {nodesdb: desktop.settings.nodesdb, from: id, to: pid}),
                function () {
                    waterfall([
                        ajax_get_first_in_async_waterfall("getnode", {nodesdb: desktop.settings.nodesdb, id: pid}),
                        function (x) {
                            curnode = x;
                            setTimeout(function () {tree.refreshItem(yid);}, 0);
                            setTimeout(function () {tree.refreshItem(xid);}, 0);
                            menu.clearAll();
                        }
                    ]);
                }
            ]);
        }
        if (desktop.mouseevent.ctrlKey || desktop.mouseevent.shiftKey) {
            waterfall([
                ajax_get_first_in_async_waterfall("compareaddnode", {nodesdb: desktop.settings.nodesdb, from: id, to: pid}),
                function () {
                    waterfall([
                        ajax_get_first_in_async_waterfall("getnode", {nodesdb: desktop.settings.nodesdb, id: pid}),
                        function (x) {
                            curnode = x;
                            setTimeout(function () {tree.refreshItem(yid);}, 0);
                            setTimeout(function () {tree.refreshItem(xid);}, 0);
                            menu.clearAll();
                        }
                    ]);
                }
            ]);
        }
        if (desktop.mouseevent.metaKey) {
            waterfall([
                ajax_get_first_in_async_waterfall("linkfathernode", {nodesdb: desktop.settings.nodesdb, from: id, to: pid}),
                function () {
                    waterfall([
                        ajax_get_first_in_async_waterfall("getnode", {nodesdb: desktop.settings.nodesdb, id: pid}),
                        function (x) {
                            curnode = x;
                            setTimeout(function () {tree.refreshItem(yid);}, 0);
                            setTimeout(function () {tree.refreshItem(xid);}, 0);
                            menu.clearAll();
                        }
                    ]);
                }
            ]);
        }
    });
    tree.attachEvent("onXLE", function () {
        if (rootid !== null && trashid === null) {
            _.each(tree.getSubItems(rootid), function (e) {
                if (tree.getUserData(e, "type") === "T") {
                    trashid = e;
                }
            });
        }
        if (rootid === null) {
            rootid = tree.getSubItems(undefined)[0];
        }
    });
    let contextmenu = new dhtmlXMenuObject({
        context: true,
        items: [
            {id: "itemText"},
            {type: "separator"},
            {id: "upload", text: "Upload"},
            {type: "separator"},
            {id: "create_node", text: "Create node"},
            {id: "rename_node", text: "Rename node"},
            {id: "duplicate_node", text: "Duplicate node"},
            {id: "delete_node", text: "Delete node"},
            {id: "refresh_node", text: "Refresh node"},
            {id: "edit_live_object", text: "Edit Live Object"},
            {type: "separator"},
            {id: "open_node", text: "Open node"},
            {type: "separator"},
            {id: "execute_query", text: "Execute query"},
            {id: "run_chart", text: "Run chart"},
            {id: "run_choice", text: "Run choice"},
            {type: "separator"},
            {id: "clear_cache", text: "Clear cache"},
            {id: "clear_progeny_caches", text: "Clear progeny caches"},
            {id: "build_progeny_caches", text: "Build progeny caches"},
            {type: "separator"},
            {id: "display_collection", text: "Display collection"},
            {type: "separator"},
            {id: "download", text: "Download"},
            {id: "downloadc", text: "Download children"},                
            {id: "display_member", text: "Display member"},
            {id: "unload", text: "Unload"},
            {type: "separator"},
            {id: "export", text: "Export database"},
            {id: "import", text: "Import database"},
            {type: "separator"},
            {id: "empty_trash", text: "Empty trash"},
        ]
    });
    contextmenu.setIconset("awesome");
    contextmenu.setItemImage("upload","fa fa-upload", "fa fa-upload");
    contextmenu.setItemImage("create_node","fa fa-magic", "fa fa-magic");
    contextmenu.setItemImage("rename_node","fa fa-pencil", "fa fa-pencil");
    contextmenu.setItemImage("duplicate_node","fa fa-copy", "fa fa-copy");
    contextmenu.setItemImage("delete_node","fa fa-trash", "fa fa-trash");
    contextmenu.setItemImage("refresh_node","fa fa-refresh", "fa fa-refresh");
    contextmenu.setItemImage("edit_live_object","fa fa-pencil", "fa fa-pencil");
    contextmenu.setItemImage("open_node","fa fa-hand-o-right", "fa fa-hand-o-right");
    contextmenu.setItemImage("execute_query","fa fa-question", "fa fa-question");
    contextmenu.setItemImage("run_chart","fa fa-line-chart", "fa fa-line-chart");
    contextmenu.setItemImage("run_choice","fa fa-sitemap", "fa fa-sitemap");
    contextmenu.setItemImage("download","fa fa-download", "fa fa-download");
    contextmenu.setItemImage("downloadc","fa fa-download", "fa fa-download");
    contextmenu.setItemImage("display_collection","fa fa-file-text", "fa fa-file-text");
    contextmenu.setItemImage("display_member","fa fa-file-text", "fa fa-file-text");
    contextmenu.setItemImage("unload","fa fa-cloud-download", "fa fa-cloud-download");
    contextmenu.setItemImage("clear_cache","fas fa-angle-double-down", "fas fa-angle-double-down");
    contextmenu.setItemImage("clear_progeny_caches","fas fa-angle-double-down", "fas fa-angle-double-down");
    contextmenu.setItemImage("build_progeny_caches","fas fa-angle-double-up", "fas fa-angle-double-up");
    contextmenu.setItemImage("export","fa fa-sign-out", "fa fa-sign-out");
    contextmenu.setItemImage("import","fa fa-sign-in", "fa fa-sign-in");
    contextmenu.setItemImage("empty_trash","fa fa-trash-o", "fa fa-trash-o");
    menu.attachEvent("onClick", function(id) {
        if (menu.actions[id].action === "dispchart") {
            dispchart(curnode, menu.actions[id].chart);
        }
        if (menu.actions[id].action === "dispchoice") {
            dispchoice(curnode, menu.actions[id].choice);
        }
    });
    tree.attachEvent("onSelect", function(id, select){
        if (select) {
            let type = tree.getUserData(id, "type");
            let contextmenuenabled = {upload: false, create_node: true, rename_node: false, edit_live_object: false, delete_node: false, duplicate_node: false, refresh_node: true, open_node: true, execute_query: false, run_chart: false, run_choice: false, download: false, downloadc: true, display_member: false, unload: false, export: false, import:false, clear_progeny_caches: false, build_progeny_caches: false, empty_trash: false};
            if (id == rootid) {
                contextmenuenabled.export = true;
                contextmenuenabled.import = true;    
            }
            if (_.contains(["N", "B", "A", "C", "D", "L"], type)) {
                contextmenuenabled.clear_cache = true;
                contextmenuenabled.clear_progeny_caches = true;
                contextmenuenabled.build_progeny_caches = true;
            }
            if (_.contains(["B", "N"], type)) {
                contextmenuenabled.upload = true;
            }
            if (_.contains(["A", "B", "C", "D", "L", "N"], type)) {
                contextmenuenabled.rename_node = true;
                contextmenuenabled.delete_node = true;
            }
            if (_.contains(["A", "B", "C", "D"], type)) {
                contextmenuenabled.execute_query = true;
                contextmenuenabled.run_chart = true;
                contextmenuenabled.run_choice = true;
            }
            if (_.contains(["B"], type)) {
                contextmenuenabled.download = true;
                contextmenuenabled.display_member = true;
            }
            if (_.contains(["A", "B", "D"], type)) {
                contextmenuenabled.unload = true;
            }
            if (_.contains(["D"], type)) {
                contextmenuenabled.duplicate_node = true;    
                contextmenuenabled.edit_live_object = true;    
            }
            if (_.contains(["T"], type)) {
                contextmenuenabled.empty_trash = true;
            }
            
            _.each(contextmenuenabled, function (v, k) {
                if (v) {
                    contextmenu.setItemEnabled(k);
                } else {
                    contextmenu.setItemDisabled(k);
                }
            });
            menu.clearAll();
            menu.actions = {};
            waterfall([
                ajax_get_first_in_async_waterfall("getnode", {nodesdb: desktop.settings.nodesdb, id: id}),
                function (node) {
                    curnode = node;
                    if (_.contains(["A", "B", "C", "D"], type)) {
                        _.each(potentialmenus, function (m) {
                            if (_.contains(_.keys(node.datasource.collections), m.tablecondition)) {
                                if (menu.getItemType(m.id) === null) {
                                    menu.addNewSibling(null, m.id, m.label);
                                    menu.setItemImage(m.id, m.icon, m.icon);
                                    gensubmenus(menu, m.items, m.id, node);
                                }
                            }
                        });
                    }
                }
            ]);
        }
    });
    tree.attachEvent("onContextMenu", function(id, x, y, ev) {
        contextmenu.setItemText("itemText", "Node: " + tree.getItemText(id));
        contextmenu.showContextMenu(x, y);
        tree.selectItem(id);
        log.debug("onContextMenu event, id: " + id + " (" + tree.getItemText(id) + ")");
        if (onclick !== null) {
            contextmenu.detachEvent(onclick);
        }
        onclick = contextmenu.attachEvent("onClick", function (fid) {
            if (fid === "upload") {
                log.debug("Upload on item: " + id + " (" + tree.getItemText(id) + ")");
                upload(makeURL("uploadnode", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id}), function () {
                    tree.loadStruct("gettree?nodesdb=" + desktop.settings.nodesdb + "&id=" + id);
                });
            }
            if (fid === "create_node") {
                log.debug("Create node within item: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("createnode", {nodesdb: desktop.settings.nodesdb, id: id}),
                    function (x) {
                        tree.loadStruct("gettree?nodesdb=" + desktop.settings.nodesdb + "&id=" + id).then(function(){
                            tree.selectItem(x.id);
                        }).then(function() {
                            let oldname = tree.getItemText(x.id);
                            let aftergetnewname = function(name) {
                            if (name !== oldname) {
                                waterfall([
                                    ajax_get_first_in_async_waterfall("renamenode", {nodesdb: desktop.settings.nodesdb, id: x.id, new: name}),
                                    function (x) {
                                        tree.setItemText(x.id, name);
                                    }
                                ]);
                            }
                         };
                        rename(oldname, aftergetnewname);
                        });
                    }
                ]);
            }
            if (fid === "rename_node") {
                log.debug("Rename node: " + id + " (" + tree.getItemText(id) + ")");
                let oldname = tree.getItemText(id);
                let aftergetnewname = function(name) {
                    if (name !== oldname) {
                        waterfall([
                            ajax_get_first_in_async_waterfall("renamenode", {nodesdb: desktop.settings.nodesdb, id: id, new: name}),
                            function (x) {
                                tree.setItemText(id, name);
                            }
                        ]);
                    }
                };
                rename(oldname, aftergetnewname);
            }
            if (fid === "duplicate_node") {
                log.debug("Duplicate node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("duplicatenode", {nodesdb: desktop.settings.nodesdb, id: id}),
                    function (x) {
                        tree.loadStruct("gettree?nodesdb=" + desktop.settings.nodesdb + "&id=" + tree.getParentId(id)).then(function(){
                            tree.selectItem(x.id);
                        }).then(function() {
                            let oldname = tree.getItemText(x.id);
                            let aftergetnewname = function(name) {
                            if (name !== oldname) {
                                waterfall([
                                    ajax_get_first_in_async_waterfall("renamenode", {nodesdb: desktop.settings.nodesdb, id: x.id, new: name}),
                                    function (x) {
                                        tree.setItemText(x.id, name);
                                    }
                                ]);
                            }
                         };
                        rename(oldname, aftergetnewname);
                        });
                    }
                ]);
            }                
            if (fid === "edit_live_object") {
                log.debug("Edit live object attached to node: " + id + " (" + tree.getItemText(id) + ")");
                let loname = null;
                waterfall([
                    ajax_get_first_in_async_waterfall("getnode", {nodesdb: desktop.settings.nodesdb, id: id}),
                    function (node) {
                        loname = node.datasource.liveobject;
                        edit_object(true, loname, desktop.settings.nodesdb, id);
                    }
                ]);
            }
            if (fid === "delete_node") {
                log.debug("Delete node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("deletenode", {nodesdb: desktop.settings.nodesdb, id: id}),
                    function (x) {
                        tree.deleteItem(id);
                        tree.refreshItem(trashid);                           
                    }
                ]);
            }
            if (fid === "refresh_node") {
                log.debug("Refresh node:" + id + " (" + tree.getItemText(id) + ")");
                tree.refreshItem(trashid);                           
            }
            if (fid === "open_node") {
                log.debug("Open node: " + id + " (" + tree.getItemText(id) + ")");
                manage_node(tree, id, curnode);
            }
            if (fid === "execute_query") {
                log.debug("Execute query on node: " + id + " (" + tree.getItemText(id) + ")");
                execute_query(tree, curnode);
            }
            if (fid === "run_chart") {
                log.debug("Running chart on node: " + id + " (" + tree.getItemText(id) + ")");
                run_chart(curnode);
            }
            if (fid === "run_choice") {
                log.debug("Running choice on node: " + id + " (" + tree.getItemText(id) + ")");
                run_choice(curnode);
            }
            if (fid === "download") {
                log.debug("Download at node: " + id + " (" + tree.getItemText(id) + ")");
                window.location.href = '/downloadsource?id=' + encodeURIComponent(id) + '&nodesdb=' + desktop.settings.nodesdb;
            }
            if (fid === "downloadc") {
                log.debug("Download children at node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("getBchildren", {nodesdb: desktop.settings.nodesdb, id: id}),
                    function (x) {
                        let download_files = function (f) {
                            let download_next = function (i) {
                                if (i >= f.length) {
                                    return;
                                }
                                let a = document.createElement('a');
                                a.href = f[i].download;
                                a.target = '_parent';
                                (document.body || document.documentElement).appendChild(a);
                                a.click();
                                a.parentNode.removeChild(a);
                                setTimeout(function() {
                                    download_next(i + 1);
                                }, 5000);
                            };
                            download_next(0);
                        };
                        let list = [];
                        _.each(x, function (nid) {
                            list.push({download: '/downloadsource?id=' + encodeURIComponent(nid) + '&nodesdb=' + desktop.settings.nodesdb});
                        });
                        download_files(list);
                    }
                ]);
            }
            if (fid === "display_member") {
                log.debug("Display member at node: " + id + " (" + tree.getItemText(id) + ")");
                let aftergetchoice = function(member) {
                    waterfall([
                        ajax_get_first_in_async_waterfall("getmember", {nodesdb: desktop.settings.nodesdb, id: id, member: member}),
                        function (x) {
                            let wmem = create_window("display_member", tree.getItemText(id) + ' / ' + member);
                            let uniqueid = _.uniqueId('display_member');
                            wmem.attachHTMLString('<div id="' + uniqueid + '" style="width:100%;height:100%;overflow:auto">' + x + '</div>');
                        }
                    ]);
                };
                waterfall([
                    ajax_get_first_in_async_waterfall("getmemberlist", {nodesdb: desktop.settings.nodesdb, id: id}),
                    function (x) {
                        let listmembers = [];
                        _.each(_.sortBy(getallchoices(x, tree.getUserData("type")), function(c) {
                            return c;
                        }), function(c) {
                            listmembers.push({text: c, value: c, selected: false});
                        });
                        getchoice(listmembers, aftergetchoice);
                    }
                ]);
            }
            if (fid === "display_collection") {
                log.debug("Display collection at node: " + id + " (" + tree.getItemText(id) + ")");
                let aftergetcollectionslist = function(collection) {
                    waterfall([
                        ajax_get_first_in_async_waterfall("displaycollection", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id, collection: collection}),
                        function (x) {
                            let wq = create_window("display_collection", collection);
                            let gq =wq.attachGrid();
                            let header = '';
                            let colsorting = '';
                            let filter = '';
                            _.each(x[0], function (v, k) {
                                header += k + ',';
                                colsorting += typeof(v) === 'string' ? 'str,' : 'int,';
                                filter += '#text_filter,';
                            });
                            gq.setHeader(header.slice(0, -1));
                            gq.setColSorting(colsorting.slice(0, -1));
                            gq.attachHeader(filter.slice(0, -1));
                            gq.init();
                            gq.enableSmartRendering(true);
                            gq.clearAll();
                            let datarows = [];
                            let id = 0;
                            _.each(x, function (e) {
                                let data = [];
                                _.each(e, function (v, k) {
                                    data.push(v);
                                });
                                datarows.push({id:id, data:data});
                                id += 1;
                            });
                            gq.parse({rows: datarows}, "json");
                        }
                    ]);
                };
                waterfall([
                    ajax_get_first_in_async_waterfall("getcollections", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id}),
                    function (x) {
                        let listcollections = [];
                        _.each(_.sortBy(getallchoices(x, tree.getUserData("type")), function(c) {
                            return c;
                        }), function(c) {
                            listcollections.push({text: c, value: c, selected: false});
                        });
                        getchoice(listcollections, aftergetcollectionslist);
                    }
                ]);
            }
            if (fid === "unload") {
                log.debug("Unload at node: " + id + " (" + tree.getItemText(id) + ")");
                window.location.href = '/unload?id=' + encodeURIComponent(id) + '&nodesdb=' + desktop.settings.nodesdb + '&systemdb=' + desktop.settings.systemdb;
            }
            if (fid === "export") {
                log.debug("Export at node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("export", {nodesdb: desktop.settings.nodesdb}),
                    function (x) {
                        alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    }
                ]);
            }
            if (fid === "import") {
                log.debug("Import at node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("import", {nodesdb: desktop.settings.nodesdb}),
                    function (x) {
                        alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    }
                ]);
            }
            if (fid === "clear_cache") {
                log.debug("Clear cache at node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("clearcollectioncache", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id}),
                    function (x) {
                        alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    }
                ]);
            }
            if (fid === "clear_progeny_caches") {
                log.debug("Clear progeny caches at node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("clearprogenycaches", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id}),
                    function (x) {
                        alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    }
                ]);
            }
            if (fid === "build_progeny_caches") {
                log.debug("Build progeny caches at node: " + id + " (" + tree.getItemText(id) + ")");
                waterfall([
                    ajax_get_first_in_async_waterfall("buildprogenycaches", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: id}),
                    function (x) {
                        alertify.success('<div style="font-size:150%;">' + x.msg + "</div>");
                    }
                ]);
            }
            if (fid === "empty_trash") {
                log.debug("Empty trash");
                waterfall([
                    ajax_get_first_in_async_waterfall("emptytrash", {nodesdb: desktop.settings.nodesdb}),
                    function () {
                        _.each(tree.getSubItems(id), function (e) {
                            tree.deleteItem(e);
                        });
                        tree.loadStruct("gettree?nodesdb=" + desktop.settings.nodesdb + "&id=" + id);
                    }
                ]);
            }
        });
        return false;
    });
    waterfall([
        ajax_get_first_in_async_waterfall("getmenus", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb}),
        function (menus) {
            potentialmenus = menus;
        }
    ]);
};

let dispchart = function (node, chart) {
    let uniquecid = _.uniqueId('');
    let wchart = null;
    let toggle = false;
    wchart = create_window("chart", node.name + ' - ' + chart);
    let runchart = function() {
        wchart.attachHTMLString('<div id="' + uniquecid + '" style="width:100%;height:100%;overflow:auto;text-align:center;"><img src="resources/ajax-loader.gif" alt="Work in progress..."></div>');
        waterfall([
            ajax_get_first_in_async_waterfall("runchart", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: node.id, chart: chart, width: wchart.cell.clientWidth, height: wchart.cell.clientHeight, top: desktop.settings.top, plotorientation: desktop.settings.plotorientation, colors: desktop.settings.colors, toggle: toggle, template: desktop.settings.template, variables: JSON.stringify(desktop.variables)}),
            function (x) {
                wchart.attachHTMLString('<div id="' + uniquecid + '" style="width:100%;height:100%;overflow:auto;text-align:center;"></div>');
                let chartdiv = document.getElementById(uniquecid);
                let config = {
                    showEditInChartStudio: true,
                    plotlyServerURL: "https://chart-studio.plotly.com"
                  };
                Plotly.newPlot(chartdiv, x.chart.figure, config);
                chartdiv.on('plotly_click', function(data){
                    item = data.points[0].data.legendgroup;
                    if (x.chart.events[item].onclick !== null) {
                        desktop.variables[x.chart.events[item].onclick.variable] = item;
                        if (x.chart.events[item].onclick.action === 'dispchart') {
                            dispchart(node, x.chart.events[item].onclick.chart);
                        }
                    }
                    if (x.chart.events[item].info !== null) {
                        desktop.variables[x.chart.events[item].info.variable] = item;
                        waterfall([
                            ajax_get_first_in_async_waterfall("executequery", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: node.id, query: x.chart.events[item].info.query, top: desktop.settings.top, variables: JSON.stringify(desktop.variables)}),
                            function (y) {
                                alertify.set({ delay: 15000 });
                                let key = node.datasource.type === 'C' ? y[0][0] === undefined ?  y[1][0] === undefined ? y[2][0] === undefined ? y[3][0].key : y[2][0].key : y[1][0].key : y[0][0].key : y[0].key;
                                let value = node.datasource.type === 'C' ? y[0][0] === undefined ?  y[1][0] === undefined ? y[2][0] === undefined ? y[3][0].value : y[2][0].value : y[1][0].value : y[0][0].value : y[0].value;
                                alertify.log(key + "<hr/>" + value);
                                console.log(key);
                                console.log(value);
                            }
                        ]);
                    }
                });
                chartdiv.on('plotly_legendclick', function(data){
                    navigator.clipboard.writeText(data.data[data.curveNumber].legendgroup);
                });
                chartdiv.on('plotly_doubleclick', function(data){
                    console.log(x.chart.figure);
                    toggle = !toggle;
                    runchart();
                });
                chartdiv.on('plotly_hover', function(data){
                    item = data.points[0].data.legendgroup;
                    if (x.chart.events[item].onclick !== null) {
                        _.each(document.getElementsByClassName('nsewdrag'), function (v,k) {
                            v.style.cursor = "pointer";
                        });
                    }
                    if (x.chart.events[item].info !== null) {
                        _.each(document.getElementsByClassName('nsewdrag'), function (v,k) {
                            v.style.cursor = "help";
                        });
                    }
                });
                chartdiv.on('plotly_unhover', function(){
                    _.each(document.getElementsByClassName('nsewdrag'), function (v,k) {
                        v.style.cursor = "";
                    });
            });
            }
        ]);
    };
    wchart.attachEvent("onResizeFinish", function () {
        runchart();
    });
    runchart();
};
    
let dispchoice = function (node, choice) {
    parallel({
        choice: ajax_get_in_async_parallel("getchoice", {choice: choice, systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb, variables: JSON.stringify(desktop.variables)}),
    }, function (x) {
        let callback = function (c) {
            desktop.variables[x.choice.id] = c;
            if (x.choice.action === 'dispchart') {
                dispchart(node, x.choice.chart);
            }
            if (x.choice.action === 'dispchoice') {
                dispchoice(node, x.choice.choice);
            }
        };
        waterfall([
            ajax_get_first_in_async_waterfall("executequery", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, id: node.id, query: x.choice.query, top: desktop.settings.top, variables: JSON.stringify(desktop.variables)}),
            function (y) {
                let options = [];
                _.each(_.sortBy(getallchoices(y, node.datasource.type), function(c) {
                    return c;
                }), function(v) {
                    options.push({text: v, value: v, selected: false});
                });
                getchoice(options, callback);
            }
        ]);
    });
};

let dispquery = function (tree, node, query) {
    waterfall([
        ajax_get_first_in_async_waterfall("executequery", {nodesdb: desktop.settings.nodesdb, systemdb: desktop.settings.systemdb, query: query, id: node.id, top: desktop.settings.top, variables: JSON.stringify(desktop.variables)}),
        function (x) {
            let wq = create_window("query", query + ' - ' + desktop.settings.nodesdb + ':' + tree.getPath(node.id));
            let gq =wq.attachGrid();
            let header = '';
            let colsorting = '';
            let filter = '';
            _.each(x[0], function (v, k) {
                header += k + ',';
                colsorting += typeof(v) === 'string' ? 'str,' : 'int,';
                filter += '#text_filter,';
            });
            gq.setHeader(header.slice(0, -1));
            gq.setColSorting(colsorting.slice(0, -1));
            gq.attachHeader(filter.slice(0, -1));
            gq.init();
            gq.enableSmartRendering(true);
            gq.clearAll();
            let datarows = [];
            let id = 0;
            _.each(x, function (e) {
                let data = [];
                _.each(e, function (v, k) {
                    data.push(v);
                });
                datarows.push({id:id, data:data});
                id += 1;
            });
            gq.parse({rows: datarows}, "json");
        }
    ]);
};

let run_choice = function (node) {
    parallel({
        list: ajax_get_in_async_parallel("getchoices", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
    }, function (x) {
        let callback = function (c) {
            dispchoice(node, c);
        };
        let options = [];
        _.each(_.sortBy(x.list, function(e) {
            return e.id;
        }), function(c) {
            options.push({text: c.id, value: c.id, selected: false});
        });
        options = _.uniq(options, function (e) {
            return e.text;
        });
        getchoice(options, callback);
    });
};

let run_chart = function (node) {
    parallel({
        list: ajax_get_in_async_parallel("getcharts", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
    }, function (x) {
        let callback = function (c) {
            dispchart(node, c);
        };
        let options = [];
        _.each(_.sortBy(x.list, function(e) {
            return e.id;
        }), function(c) {
            options.push({text: c.id, value: c.id, selected: false});
        });
        options = _.uniq(options, function (e) {
            return e.text;
        });
        getchoice(options, callback);
    });
};

let execute_query = function (tree, node) {
    parallel({
        list: ajax_get_in_async_parallel("getqueries", {systemdb: desktop.settings.systemdb, nodesdb: desktop.settings.nodesdb}),
    }, function (x) {
        let callback = function (c) {
            dispquery(tree, node, c);
        };
        let options = [];
        _.each(_.sortBy(x.list, function(e) {
            return e.id;
        }), function(c) {
            options.push({text: c.id, value: c.id, selected: false});
        });
        options = _.uniq(options, function (e) {
            return e.text;
        });
        getchoice(options, callback);
    });
};

let load = function () {
    // initMainLayout
    desktop.layout = new dhtmlXLayoutObject(document.body,"1C");
    desktop.layout.cells("a").hideHeader();
    desktop.layout.cells("a").setBI("resources/DEFAULT.jpg");
    desktop.windows = new dhtmlXWindows();
    desktop.layout.attachEvent("onPanelResizeFinish", function(cells){
        for (let q=0; q<cells.length; q++) {
            if (cells[q] == "a") {
                desktop.windows.forEachWindow(function(win){
                    win.adjustPosition();
                });
            }
        }
    });
    desktop.toolbar = desktop.layout.cells("a").attachToolbar();
    desktop.toolbar.setIconset("awesome");
    let toolbardata = [
        {type: "buttonSelect", id: "kairos", text: "KAIROS", title: "KAIROS", openAll: true, img: "fa fa-home yellow", options: [
            {type: "obj", id: "kairos_log", text: "KAIROS log", img: "fa fa-file-text-o yellow"},
            {type: "obj", id: "postgres_logfile", text: "PostgreSQL log", img: "fa fa-file-text-o"},
            {type: "obj", id: "webserver_log", text: "WEBSERVER log", img: "fa fa-file-text-o"},
            {type: "separator"},
            {type: "obj", id: "documentation", text: "KAIROS documentation", img: "fa fa-file-pdf-o"},
            {type: "separator"},
            {type: "obj", id: "explorer", text: "Explorer", img: "fa fa-university"},
            {type: "separator"},
            {type: "obj", id: "manage_objects", text: "Manage objects", img: "fa fa-spinner"},
            {type: "separator"},
            {type: "obj", id: "list_databases", text: "List databases", img: "fa fa-database"},
            {type: "separator"},
            {type: "obj", id: "manage_roles", text: "Manage roles", img: "fa fa-users"},
            {type: "obj", id: "manage_users", text: "Manage users", img: "fa fa-user"},
            {type: "obj", id: "manage_grants", text: "Manage grants", img: "fa fa-book"},
            {type: "obj", id: "manage_password", text: "Manage password", img: "fa fa-key"},
            {type: "separator"},
            {type: "obj", id: "settings", text: "Settings", img: "fa fa-cog"},
            {type: "separator"},
            {type: "obj", id: "logout", text: "Logout", img: "fa fa-sign-out"}
        ]},
        {type: "separator"},
        {type: "button", id: "settings", title: "Settings", img: "fa fa-cog"},
        {type: "button", id: "explorer", title: "Explorer", img: "fa fa-university"},
        {type: "button", id: "wminimize", title: "Minize all windows", img: "fa fa-arrow-down"},
        {type: "button", id: "wclose", title: "Close all windows", img: "fa fa-close"},
        {type: "separator"},
        {type: "buttonSelect", id: "windows", text: "Windows", title: "Windows", openAll: true, img: "fa fa-th-list", options: [
        ]}
    ];
    desktop.toolbar.loadStruct(toolbardata);
    desktop.toolbar.attachEvent("onClick", function(id){
        if (id === "kairos_log") {
            kairos_log();
        }
        if (id === "postgres_logfile") {
            postgres_logfile();
        }
        if (id === "webserver_log") {
            webserver_log();
        }
        if (id === "documentation") {
            documentation();
        }
        if (id === "manage_objects") {
            manage_objects();
        }
        if (id === "list_databases") {
            list_databases();
        }
        if (id === "manage_roles") {
            manage_roles();
        }
        if (id === "manage_users") {
            manage_users();
        }
        if (id === "manage_grants") {
            manage_grants();
        }
        if (id === "manage_password") {
            manage_password();
        }
        if (id === "settings") {
            settings();
        }
        if (id === "explorer") {
            explorer();
        }
        if (id === "wminimize") {
            desktop.windows.forEachWindow(function (w) {
                if (!w.isParked()) {
                    w.hide();
                    w.park();
                }
            });
        }
        if (id === "wclose") {
            desktop.windows.forEachWindow(function (w) {
                w.close();
            });

        }
        if (id === "logout") {
            window.location.reload();
        }
        if (desktop.toolbar.getParentId(id) === "windows") {
            let win = desktop.windows.window(id);
            win.show();
            win.bringToTop();
            if (win.isParked()) {
                win.park();
            }
        }
    });
    desktop.statusbar = desktop.layout.cells("a").attachStatusBar({height: 20, text:''});
    desktop.statusbar.style.backgroundColor = "lightskyblue";
    desktop.layout.cells("a").hideToolbar();

    let loginform = function(x) {
        document.title = `KAIROS V${VERSION}`;
        login(x);
    };

    waterfall([
        ajax_get_first_in_async_waterfall("checkserverconfig"),
        ajax_get_next_in_async_waterfall("listusers"),
        loginform
    ]);
};
dhtmlxEvent(window,"load",load);
