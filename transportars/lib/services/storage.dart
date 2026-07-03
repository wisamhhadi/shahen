import 'package:get_storage/get_storage.dart';

class AppStorage {
  static final GetStorage _box = GetStorage();

  static String? get token => _box.read('transporter_token');
  static int? get transporterId => _box.read('transporter_id');

  static Future<void> saveAuth(String token, int id) async {
    await _box.write('transporter_token', token);
    await _box.write('transporter_id', id);
  }

  static Future<void> clear() async {
    await _box.remove('transporter_token');
    await _box.remove('transporter_id');
  }
}
