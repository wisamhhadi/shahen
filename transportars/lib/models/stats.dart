class Stats {
  final int drivers;
  final int vehicles;
  final int orders;
  final int activeOrders;
  final int help;
  final int stopped;
  final int late;
  final int maintenance;
  final int committed;

  Stats({
    required this.drivers,
    required this.vehicles,
    required this.orders,
    required this.activeOrders,
    required this.help,
    required this.stopped,
    required this.late,
    required this.maintenance,
    required this.committed,
  });

  factory Stats.fromJson(Map<String, dynamic> json) {
    int n(String key) => int.tryParse('${json[key] ?? 0}') ?? 0;

    return Stats(
      drivers: n('drivers_count'),
      vehicles: n('vehicles_count'),
      orders: n('orders_count'),
      activeOrders: n('active_orders_count'),
      help: n('drivers_need_help_count'),
      stopped: n('stopped_drivers_count'),
      late: n('late_loading_drivers_count'),
      maintenance: n('maintenance_vehicles_count'),
      committed: n('committed_vehicles_count'),
    );
  }
}
