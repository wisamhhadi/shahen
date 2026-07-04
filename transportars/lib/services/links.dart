class Links {
  static const String server = "https://shahen.onrender.com";
  static const String base = "$server/api/";

  static const String login = "${base}transporters/login/";
  static const String me = "${base}transporters/me/";
  static const String stats = "${base}transporters/stats/";

  static const String drivers = "${base}transporters/drivers/";
  static const String createDriver = "${base}transporters/drivers/create/";

  static const String vehicles = "${base}transporters/vehicles/";
  static const String createVehicle = "${base}transporters/vehicles/create/";

  static const String orders = "${base}transporters/orders/";
  static const String wallet = "${base}transporters/wallet/";
  static const String sendNotification = "${base}transporters/notifications/send/";

  static String assignOrder(int orderId) {
    return "${base}transporters/orders/$orderId/assign/";
  }
}
