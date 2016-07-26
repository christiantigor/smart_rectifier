var wsurl = "phpScripts";
var wsurlx = "data";
var haServices = angular.module('haServices', [ 'ngResource' ]);

function createResource($resource, url, method) {
	if (method == "GET") {
		return $resource(wsurl + url, {}, {
			retrieve : {
				method : method,
				params : {},
				isArray : false
			}
		});
	} else {
		return $resource(wsurl + url, {}, {
			execute : {
				method : method,
				params : {},
				isArray : false
			}
		});
	}
}

haServices.factory("MainSvc", [ "$resource", function($resource) {
	return {
		mac : function() {
			return createResource($resource, "/getMAC.php", "GET");
		},
		sensorData : function() {
			return createResource($resource, "/getSensorData.php", "GET");
		},
		network : function() {
			return createResource($resource, "/getNetwork.php", "GET");
		},
		setnetwork : function() {
			return createResource($resource, "/setNetwork.php", "GET");
		},
		devicename : function() {
			return createResource($resource, "/getDeviceName.php", "GET");
		},
		setdevicename : function() {
			return createResource($resource, "/setDeviceName.php", "GET");
		},
		shutdown : function() {
			return createResource($resource, "/shutdown.php", "GET");
		},
		reboot : function() {
			return createResource($resource, "/reboot.php", "GET");
		},
		table : function() {
			return $resource(wsurl + "/getTableData.php", {}, {
				retrieve : {
					method : "GET",
					params : {},
					isArray : true
				}
			});
		},
		graph : function() {
			return $resource(wsurl + "/getGraphData.php", {}, {
				retrieve : {
					method : "GET",
					params : {},
					isArray : true
				}
			});
		}
	};
} ]);