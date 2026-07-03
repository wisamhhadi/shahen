class TransporterStats {
  final int driversCount;
  final int vehiclesCount;
  final int ordersCount;
  final int activeOrdersCount;
  final int completedOrdersCount;
  final int rejectedOrdersCount;
  final int committedVehiclesCount;
  final int driversNeedHelpCount;
  final int stoppedDriversCount;
  final int lateLoadingDriversCount;
  final int maintenanceVehiclesCount;

  TransporterStats({
    required this.driversCount,
    required this.vehiclesCount,
    required this.ordersCount,
    required this.activeOrdersCount,
    required this.completedOrdersCount,
    required this.rejectedOrdersCount,
    required this.committedVehiclesCount,
    required this.driversNeedHelpCount,
    required this.stoppedDriversCount,
    required this.lateLoadingDriversCount,
    required this.maintenanceVehiclesCount,
  });

  factory TransporterStats.fromJson(Map<String, dynamic> json) {
    int n(String key) => int.tryParse("${json[key] ?? 0}") ?? 0;
    return TransporterStats(
      driversCount: n("drivers_count"),
      vehiclesCount: n("vehicles_count"),
      ordersCount: n("orders_count"),
      activeOrdersCount: n("active_orders_count"),
      completedOrdersCount: n("completed_orders_count"),
      rejectedOrdersCount: n("rejected_orders_count"),
      committedVehiclesCount: n("committed_vehicles_count"),
      driversNeedHelpCount: n("drivers_need_help_count"),
      stoppedDriversCount: n("stopped_drivers_count"),
      lateLoadingDriversCount: n("late_loading_drivers_count"),
      maintenanceVehiclesCount: n("maintenance_vehicles_count"),
    );
  }
}
