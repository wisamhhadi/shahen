class Links {
  static const String server = "https://shahen.onrender.com";
  static const String base = "$server/api/";

  static const String login = "${base}transporters/login/";
  static const String me = "${base}transporters/me/";
  static const String stats = "${base}transporters/stats/";
  static const String drivers = "${base}transporters/drivers/";
  static const String vehicles = "${base}transporters/vehicles/";
  static const String orders = "${base}transporters/orders/?include_open=1";
  static const String wallet = "${base}transporters/wallet/";
  static const String sendNotification = "${base}transporters/notifications/send/";
  static const String logout = "${base}transporters/logout/";

  static String assignOrder(int id) => "${base}transporters/orders/$id/assign/";
}
