import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../services/links.dart';
import '../../services/network.dart';
import '../../services/storage.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final phoneController = TextEditingController();
  final passwordController = TextEditingController();
  final net = Network();
  bool loading = false;

  Future<void> login() async {
    setState(() => loading = true);

    try {
      final data = await net.postMap(Links.login, {
        "phone": phoneController.text.trim(),
        "password": passwordController.text.trim(),
      });

      await AppStorage.saveAuth(data["token"].toString(), int.tryParse("${data["id"]}") ?? 0);
      Get.offAllNamed('/home');
    } catch (e) {
      Get.snackbar("خطأ", "فشل تسجيل الدخول: $e", snackPosition: SnackPosition.BOTTOM);
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      body: Center(child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Container(
          padding: const EdgeInsets.all(22),
          decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(24), boxShadow: const [
            BoxShadow(color: Color(0x22000000), blurRadius: 16, offset: Offset(0, 8)),
          ]),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            const CircleAvatar(radius: 45, backgroundColor: Color(0xFF1E9B4B), child: Icon(Icons.local_shipping, size: 45, color: Colors.white)),
            const SizedBox(height: 16),
            const Text("تسجيل دخول الناقل", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 22)),
            const SizedBox(height: 22),
            TextField(controller: phoneController, keyboardType: TextInputType.phone, decoration: const InputDecoration(labelText: "رقم الهاتف", prefixIcon: Icon(Icons.phone), border: OutlineInputBorder())),
            const SizedBox(height: 12),
            TextField(controller: passwordController, obscureText: true, decoration: const InputDecoration(labelText: "كلمة المرور", prefixIcon: Icon(Icons.lock), border: OutlineInputBorder())),
            const SizedBox(height: 20),
            SizedBox(width: double.infinity, height: 50, child: ElevatedButton.icon(
              onPressed: loading ? null : login,
              icon: loading ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.login),
              label: Text(loading ? "جاري الدخول..." : "دخول"),
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1E9B4B), foregroundColor: Colors.white),
            )),
          ]),
        ),
      )),
    ));
  }
}
