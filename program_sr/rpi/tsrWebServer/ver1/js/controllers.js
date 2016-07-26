var haControllers = angular.module('haControllers', []);

function showLoading($mdDialog, process) {
	var loading = {
		templateUrl : "partials/loadingdialog.html",
		onComplete : process
	};

	$mdDialog.show(loading);
}

function blurs(event, element) {
	if (event.keyCode == 13) {
		element.blur();
	}
}

function showAlert($mdDialog, title, content) {
	var alert = $mdDialog.alert().clickOutsideToClose(true).title(title)
			.textContent(content).ariaLabel('Alert Dialog').ok('Tutup');

	$mdDialog.show(alert);
}

function hideLoading($mdDialog) {
	$mdDialog.hide();
}

function retrieve($scope, $mdDialog, loading, Service, input, callback,
		errorcallback) {
	if ($scope.running == null) {
		$scope.running = 0;
	}

	var process = function() {
		Service.retrieve(input, function(result) {
			callback(result);

			if (loading) {
				$scope.running--;
				if ($scope.running == 0) {
					hideLoading($mdDialog);
				}
			}
		},
				function(error) {
					if (showLoading) {
						$scope.running--;
						if ($scope.running == 0) {
							hideLoading($mdDialog);
						}
					}

					if (error.data == null) {
						showAlert($mdDialog, "",
								"Tidak dapat terhubung dengan server");
					} else {
						showAlert($mdDialog, error.status + " - "
								+ error.statusText, error.data.exception);
					}

					if (errorcallback) {
						errorcallback(error);
					}
				});
	};

	if (loading) {
		$scope.running++;
		if ($scope.running == 1) {
			showLoading($mdDialog, process);
		} else {
			process();
		}
	} else {
		process();
	}
}

haControllers
		.controller(
				'MainCtrl',
				[
						'$scope',
						'MainSvc',
						'$mdDialog',
						'$interval',
						function($scope, MainSvc, $mdDialog, $interval) {
							retrieve($scope, $mdDialog, true, MainSvc.mac(),
									{}, function(result) {
										$scope.mac = result.kodePerangkat
												.toUpperCase();
									});

							retrieve(
									$scope,
									$mdDialog,
									true,
									MainSvc.network(),
									{},
									function(result) {
										var ip = {};
										ip.address = {};
										ip.subnet = {};
										ip.gateway = {};
										ip.network = {};
										ip.broadcast = {};

										ip.address.real = result.IP;
										ip.subnet.real = result.Netmask;
										ip.gateway.real = result.Gateway;
										ip.network.real = result.Network;
										ip.broadcast.real = result.Broadcast;

										ip.address.temp = ip.address.real
												.slice();
										ip.subnet.temp = ip.subnet.real.slice();
										ip.gateway.temp = ip.gateway.real
												.slice();
										ip.network.temp = ip.network.real
												.slice();
										ip.broadcast.temp = ip.broadcast.real
												.slice();

										$scope.ip = ip;
									});

							$scope.blurr = function(data) {
								if (data.temp.trim() == "") {
									data.temp = data.real.slice();
								} else {
									data.real = data.temp.slice();
								}
							};

							retrieve($scope, $mdDialog, true, MainSvc
									.devicename(), {}, function(result) {
								$scope.devicename = {};
								$scope.devicename.real = result.DeviceName;
								$scope.devicename.temp = $scope.devicename.real
										.slice();
							});

							$scope.savename = function() {
								if ($scope.devicename.temp.trim() == "") {
									$scope.devicename.temp = $scope.devicename.real
											.slice();
								} else {
									if ($scope.devicename.real != $scope.devicename.temp) {
										$scope.devicename.real = $scope.devicename.temp
												.slice();

										retrieve(
												$scope,
												$mdDialog,
												true,
												MainSvc.setdevicename(),
												{
													newDeviceName : $scope.devicename.real
												},
												function(result) {
													if (result.status != "success") {
														showAlert($mdDialog,
																"",
																"Setting Gagal");
													}
												});
									}
								}
							};

							var refresh = function() {
								$scope.maxDate = moment();

								retrieve($scope, $mdDialog, false, MainSvc
										.sensorData(), {}, function(result) {
									var datas = result;

									var data = [];
									data.push({
										name : "Tegangan AC",
										value : datas.srVAC,
										symbol : "V",
										def : 220
									});
									data.push({
										name : "Tegangan Baterai",
										value : datas.srVBat,
										symbol : "V",
										def : 56
									});
									data.push({
										name : "Arus Baterai",
										value : datas.srIBat,
										symbol : "A"
									});
									data.push({
										name : "Arus Beban",
										value : datas.srILoad,
										symbol : "A"
									});
									data.push({
										name : "Supply 6.5V",
										value : datas.sr6V5,
										symbol : "V",
										def : 6.5
									});
									data.push({
                                                                                name : "Supply 12V",
                                                                                value : datas.sr12V,
                                                                                symbol : "V",
                                                                                def : 12
                                                                        });
									data.push({
										name : "Supply 13.5V",
										value : datas.sr13V5,
										symbol : "V",
										def : 13.5
									});
									data.push({
										name : "Supply 19.5V",
										value : datas.sr19V5,
										symbol : "V",
										def : 19.5
									});
									data.push({
										name : "Supply 24V",
										value : datas.sr24V,
										symbol : "V",
										def : 24
									});
									data.push({
										name : "Supply 48V A",
										value : datas.sr48V_A,
										symbol : "V",
										def : 48
									});
									data.push({
										name : "Supply 48V B",
										value : datas.sr48V_B,
										symbol : "V",
										def : 48
									});
									data.push({
										name : "Temperatur",
										value : datas.srTemp,
										symbol : "\u2103",
										def : 30
									});

									for ( var i = 0; i < data.length; i++) {
										var d = data[i];
										var delta = Math.abs(d.value - d.def);
										var warning = d.def * 25 / 100;
										var alert = d.def * 30 / 100;

										if (delta >= alert) {
											d.warnlevel = 2;
										} else if (delta >= warning) {
											d.warnlevel = 1;
										} else {
											d.warnlevel = 0;
										}
									}

									$scope.data = data;

								}, function(error) {
									$interval.cancel(refreshid);
								});
							};

							$scope.save = function() {
								retrieve($scope, $mdDialog, true, MainSvc
										.setnetwork(), {
									newAddress : $scope.ip.address.real,
									newNetmask : $scope.ip.subnet.real,
									newGateway : $scope.ip.gateway.real,
									newNetwork : $scope.ip.network.real,
									newBroadcast : $scope.ip.broadcast.real
								}, function(result) {
									if (result.status != "success") {
										showAlert($mdDialog, "",
												"Setting Gagal");
									}
								});
							};

							$scope.turnoff = function(ev) {
								var confirm = $mdDialog.confirm().textContent(
										'Shutdown perangkat ini?')

								.targetEvent(ev).ok('Shutdown').cancel('Batal');
								$mdDialog
										.show(confirm)
										.then(
												function() {
													retrieve(
															$scope,
															$mdDialog,
															true,
															MainSvc.shutdown(),
															{},
															function(result) {
																if (result.status != "success") {
																	showAlert(
																			$mdDialog,
																			"",
																			"Shutdown Gagal");
																} else {
																	showAlert(
																			$mdDialog,
																			"",
																			"Perangkat Anda akan segera di-shutdown");
																}
															});
												}, function() {

												});
							};

							$scope.restart = function(ev) {
								var confirm = $mdDialog.confirm().textContent(
										'Restart perangkat ini?')

								.targetEvent(ev).ok('Restart').cancel('Batal');
								$mdDialog
										.show(confirm)
										.then(
												function() {
													retrieve(
															$scope,
															$mdDialog,
															true,
															MainSvc.reboot(),
															{},
															function(result) {
																if (result.status != "success") {
																	showAlert(
																			$mdDialog,
																			"",
																			"Restart Gagal");
																} else {
																	showAlert(
																			$mdDialog,
																			"",
																			"Perangkat Anda akan segera di-restart");
																}
															});
												}, function() {

												});
							};

							var types = [];
							types.push({
								name : "Tegangan AC",
								value : 0
							});
							types.push({
								name : "Tegangan Baterai",
								value : 1
							});
							types.push({
								name : "Arus Baterai",
								value : 2
							});
							types.push({
								name : "Arus Beban",
								value : 3
							});
							types.push({
								name : "Supply 6.5V",
								value : 4
							});
							types.push({
								name : "Supply 12V",
								value : 5
							});
							types.push({
								name : "Supply 13.5V",
								value : 6
							});
							types.push({
								name : "Supply 19.5V",
								value : 7
							});
							types.push({
								name : "Supply 24V",
								value : 8
							});
							types.push({
								name : "Supply 48V_A",
								value : 9
							});
							types.push({
								name : "Supply 48V_B",
								value : 10
							});
							types.push({
								name : "Temperatur",
								value : 11
							});
							$scope.types = types;
							$scope.type = 0;
							$scope.change = function(time) {
								if (time) {
									$scope.monitorDate = moment(time);
								} else {
									$scope.monitorDate = moment($scope.monitorDate);
								}
								$scope.retrieveGraph();
							};
							$scope.minDate = moment().subtract(7, 'days');
							$scope.maxDate = moment();
							$scope.startDate = moment().subtract(7, 'days');
							$scope.endDate = moment();
							$scope.monitorDate = moment().minute(0).second(0);

							tickFormat = function(d) {
								if (d === parseInt(d, 10)) {
									var d1 = Math.floor(d / 60);
									var d2 = d % 60;

									if (d1 < 10) {
										d1 = "0" + d1;
									}

									if (d2 < 10) {
										d2 = "0" + d2;
									}

									return moment($scope.monitorDate).format(
											"HH")
											+ ":" + d1 + ":" + d2;
								} else {
									return "";
								}
							};

							yTickFormat = function(d) {
								d = d3.format(',.2f')(d);
								switch (parseInt($scope.type)) {
								case 0:
								case 1:
								case 4:
								case 5:
								case 6:
								case 7:
								case 8:
								case 9:
								case 10:
									return d + "V";
								case 2:
								case 3:
									return d + "A";
								case 11:
									return d + "\u2103";
								default:
									return d;
								}
							};

							$scope.options = {
								"chart" : {
									"type" : "lineWithFocusChart",
									"height" : 450,
									"margin" : {
										"top" : 20,
										"right" : 40,
										"bottom" : 60,
										"left" : 60
									},
									"duration" : 500,
									"useInteractiveGuideline" : true,
									"xAxis" : {
										"axisLabel" : "Waktu",
										tickFormat : tickFormat
									},
									"x2Axis" : {
										tickFormat : tickFormat
									},
									"yAxis" : {
										"axisLabel" : "",
										"rotateYLabel" : false,
										tickFormat : yTickFormat
									},
									"y2Axis" : {
										tickFormat : yTickFormat
									},
									"showLegend" : false,
									forceY:[0,0]
								}
							};

							var datax = [];
							datax.push({
								key : $scope.types[$scope.type].name,
								values : []
							});
							$scope.dota = datax;

							$scope.retrieveGraph = function() {
								var date = $scope.monitorDate
										.format("YYYY-MM-DD HH");

								retrieve(
										$scope,
										$mdDialog,
										true,
										MainSvc.graph(),
										{
											startDate : date + ":00:00",
											endDate : date + ":59:59",
											type : $scope.type
										},
										function(result) {
											$scope.dota[0].key = types[$scope.type].name;

											var datac = $scope.dota;
											datac[0].values = [];
											for ( var i = 0; i < result.length; i++) {
												var row = result[i];
												var x = parseInt(row.time
														.substring(17));
												x += (parseInt(row.time
														.substring(14, 16)) * 60);

												datac[0].values.push({
													series : 0,
													x : x,
													y : row.value
												});
											}
										});
							};
							$scope.removeGraph = function() {
								$scope.dota[0].values.splice(0,
										$scope.dota[0].length);
							};

							$scope.retrieveTable = function() {
								retrieve($scope, $mdDialog, true, MainSvc
										.table(), {}, function(result) {
									$scope.monitorDatas = result;
									$scope.page = 1;
									$scope.onPaginate(1, 50);
								});
							};
							$scope.onPaginate = function(page, limit) {
								var len = $scope.monitorDatas.length;
								var lim = limit * page;
								if(len < lim) {
									lim = len; 
								}
								
								$scope.monitorData = $scope.monitorDatas.slice(
										(page - 1) * limit, lim);
							};
							$scope.removeTable = function() {
								$scope.monitorData.splice(0,
										$scope.monitorData.length);
							};
							$scope.monitorData = [];

							$scope.$watch("selectedtab", function() {
								if ($scope.selectedtab == 1) {
									$scope.retrieveGraph();
									$scope.removeTable();
								} else if ($scope.selectedtab == 2) {
									$scope.retrieveTable();
									$scope.removeGraph();
								} else {
									$scope.removeTable();
									$scope.removeGraph();
								}

							});

							$scope.exports = function() {
								var startDate = moment($scope.startDate)
										.format("YYYY-MM-DD");
								var endDate = moment($scope.endDate).format(
										"YYYY-MM-DD");
								return "phpScripts/getCsvData.php?startDate="
										+ startDate + " 00:00:00&endDate="
										+ endDate + " 23:59:59";
							};

							refresh();
							var refreshid = $interval(refresh, 5000);
						} ]);
