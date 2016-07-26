// rows : number of rows per page
// maxPages : max navigation links shown
// count : function(filter, callback) for determining length 
// retrieve : function(first, pagesize, sortcriteria, sortorder, filter, callback) for retrieving data
function createLazyTableModel(rows, maxPages, count, retrieve) {
	var tableModel = new Object();
	tableModel.rows = rows;
	tableModel.sortCriteria = "";
	tableModel.sortOrder = "";
	tableModel.search = "";
	tableModel.maxPages = maxPages;

	tableModel.sortClass = function(sortCriteria) {
		if (tableModel.sortCriteria != sortCriteria) {
			return "glyphicon-sort";
		} else if (tableModel.sortOrder == 'asc') {
			return "glyphicon-sort-by-attributes";
		} else {
			return "glyphicon-sort-by-attributes-alt";
		}
	};

	tableModel.filter = function() {
		tableModel.navigate(0);
	};

	tableModel.sort = function(sortCriteria) {
		if (tableModel.sortCriteria == sortCriteria) {
			if (tableModel.sortOrder == "asc") {
				tableModel.sortOrder = "desc";
			} else {
				tableModel.sortOrder = "asc";
			}
		} else {
			tableModel.sortCriteria = sortCriteria;
			tableModel.sortOrder = "asc";
		}

		tableModel.navigate(tableModel.activeIndex);
	};

	tableModel.navigate = function(page) {
		var activeIndex = page;

		count(
				tableModel.search,
				function(length) {
					tableModel.length = length;
					tableModel.pages = Math.ceil(length / rows);

					tableModel.navigators = [];
					var first = 0;
					var last = tableModel.pages;
					var max = Math.floor(maxPages / 2);
					var mod = maxPages % 2;

					if (activeIndex < max + 1 && last > maxPages) {
						last = maxPages;
					} else if (activeIndex + max + mod > tableModel.pages && last > maxPages) {
						first = last - maxPages;
					} else {
						first = activeIndex - max;
						last = activeIndex + max + mod;
					}

					for ( var i = first; i < last; i++) {
						if (i >= 0 && i < tableModel.pages) {
							tableModel.navigators.push(i);
						}
					}
				});

		retrieve(activeIndex * rows, rows, tableModel.sortCriteria,
				tableModel.sortOrder, tableModel.search, function(data) {
					tableModel.data = data;
				});
		tableModel.activeIndex = activeIndex;
	};
	tableModel.navigate(0);

	tableModel.stepBackward = function() {
		tableModel.navigate(0);
	};
	tableModel.stepForward = function() {
		tableModel.navigate(tableModel.pages - 1);
	};
	tableModel.backward = function() {
		tableModel.navigate(tableModel.activeIndex - 1);
	};
	tableModel.forward = function() {
		tableModel.navigate(tableModel.activeIndex + 1);
	};

	tableModel.disableBackward = function() {
		if (tableModel.activeIndex == 0) {
			return true;
		} else {
			return false;
		}
	};
	tableModel.disableForward = function() {
		if (tableModel.activeIndex == tableModel.pages - 1) {
			return true;
		} else {
			return false;
		}
	};

	return tableModel;
}

//data : table data
//rows : number of rows per page
//maxPages : max navigation links shown
function createTableModel(data, rows, maxPages) {
	var tableModel = new Object();
	tableModel.dataPool = data.slice();
	tableModel.length = data.length;
	tableModel.rows = rows;
	tableModel.pages = Math.ceil(data.length / rows);
	tableModel.sortCriteria = "";
	tableModel.sortOrder = "";
	tableModel.search = "";
	tableModel.maxPages = maxPages;

	tableModel.sortClass = function(sortCriteria) {
		if (tableModel.sortCriteria != sortCriteria) {
			return "glyphicon-sort";
		} else if (tableModel.sortOrder == 'asc') {
			return "glyphicon-sort-by-attributes";
		} else {
			return "glyphicon-sort-by-attributes-alt";
		}
	};

	tableModel.filter = function() {
		data = tableModel.dataPool.slice();

		if (tableModel.search != "") {
			data = data.filter(function(value) {
				value = JSON.stringify(value);
				value = value.toLowerCase();
				var search = tableModel.search.toLowerCase();
				return value.indexOf(search) > -1;
			});
		}

		tableModel.pages = Math.ceil(data.length / rows);

		if (tableModel.sortCriteria != "") {
			data.sort(function(a, b) {
				var comparison = a[tableModel.sortCriteria]
						.localeCompare(b[tableModel.sortCriteria]);
				if (tableModel.sortOrder == "desc") {
					if (comparison == 0) {
						comparison = -0.1;
					} else {
						comparison *= -1;
					}
				}
				return comparison;
			});
		}

		tableModel.navigate(0);
	};

	tableModel.sort = function(sortCriteria) {
		if (tableModel.sortCriteria == sortCriteria) {
			if (tableModel.sortOrder == "asc") {
				tableModel.sortOrder = "desc";
			} else {
				tableModel.sortOrder = "asc";
			}
		} else {
			tableModel.sortCriteria = sortCriteria;
			tableModel.sortOrder = "asc";
		}

		// data = tableModel.dataPool.slice();
		data.sort(function(a, b) {
			var comparison = a[sortCriteria].localeCompare(b[sortCriteria]);
			if (tableModel.sortOrder == "desc") {
				if (comparison == 0) {
					comparison = -0.1;
				} else {
					comparison *= -1;
				}
			}
			return comparison;
		});

		tableModel.navigate(tableModel.activeIndex);
	};

	tableModel.navigate = function(page) {
		// if (tableModel.activeIndex != page) {
		var activeIndex = page;
		var activeData = [];

		for ( var i = 0; rows * activeIndex + i < data.length && i < rows; i++) {
			var temp = data[rows * activeIndex + i];
			activeData.push(temp);
		}
		tableModel.data = activeData;
		tableModel.activeIndex = activeIndex;

		tableModel.navigators = [];
		var first = 0;
		var last = tableModel.pages;
		var max = Math.floor(maxPages / 2);
		var mod = maxPages % 2;

		if (activeIndex < max + 1 && last > maxPages) {
			last = maxPages;
		} else if (activeIndex + max + mod > tableModel.pages && last > maxPages) {
			first = last - maxPages;
		} else {
			first = activeIndex - max;
			last = activeIndex + max + mod;
		}

		for ( var i = first; i < last; i++) {
			if (i >= 0 && i < tableModel.pages) {
				tableModel.navigators.push(i);
			}
		}
		// }
	};
	tableModel.navigate(0);

	tableModel.stepBackward = function() {
		tableModel.navigate(0);
	};
	tableModel.stepForward = function() {
		tableModel.navigate(tableModel.pages - 1);
	};
	tableModel.backward = function() {
		tableModel.navigate(tableModel.activeIndex - 1);
	};
	tableModel.forward = function() {
		tableModel.navigate(tableModel.activeIndex + 1);
	};

	tableModel.disableBackward = function() {
		if (tableModel.activeIndex == 0) {
			return true;
		} else {
			return false;
		}
	};
	tableModel.disableForward = function() {
		if (tableModel.activeIndex == tableModel.pages - 1) {
			return true;
		} else {
			return false;
		}
	};

	return tableModel;
}

function createFormModel(validator) {
	var object = new Object();
	object.value = "";
	object.errorStyle = "";
	object.errorMessage = "";
	object.validator = validator;
	object.valid = true;

	object.setError = function(message) {
		object.valid = false;
		object.errorStyle = "has-error";
		object.errorMessage = message;
	};

	object.setValid = function() {
		object.valid = true;
		object.errorStyle = "";
		object.errorMessage = "";
	};

	object.validate = function() {
		var message = validator(object.value);
		if (message == "") {
			object.setValid();
		} else {
			object.setError(message);
		}
	};

	return object;
}