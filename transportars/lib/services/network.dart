import 'dart:convert';
import 'package:http/http.dart' as http;
import 'storage.dart';

class Network {
  Map<String, String> get headers => {
        "Content-Type": "application/json",
        "Accept": "application/json",
        if (AppStorage.token != null) "Authorization": "Bearer ${AppStorage.token}",
      };

  Future<Map<String, dynamic>> getMap(String url) async {
    final response = await http.get(Uri.parse(url), headers: headers);
    return _handleMap(response);
  }

  Future<List<dynamic>> getList(String url) async {
    final response = await http.get(Uri.parse(url), headers: headers);
    if (response.statusCode >= 200 && response.statusCode < 300) {
      final decoded = jsonDecode(utf8.decode(response.bodyBytes));
      if (decoded is List) return decoded;
      if (decoded is Map && decoded['results'] is List) return decoded['results'];
      return [];
    }
    throw Exception("HTTP ${response.statusCode}: ${utf8.decode(response.bodyBytes)}");
  }

  Future<Map<String, dynamic>> postMap(String url, Map<String, dynamic> body) async {
    final response = await http.post(Uri.parse(url), headers: headers, body: jsonEncode(body));
    return _handleMap(response);
  }

  Map<String, dynamic> _handleMap(http.Response response) {
    final body = utf8.decode(response.bodyBytes);
    if (response.statusCode >= 200 && response.statusCode < 300) {
      final decoded = jsonDecode(body);
      if (decoded is Map<String, dynamic>) return decoded;
      return {"data": decoded};
    }
    throw Exception("HTTP ${response.statusCode}: $body");
  }
}
