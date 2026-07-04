import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../services/links.dart';
import '../../services/network.dart';

class AddDriverPage extends StatefulWidget {
  const AddDriverPage({super.key});

  @override
  State<AddDriverPage> createState() => _AddDriverPageState();
}

class _AddDriverPageState extends State<AddDriverPage> {
  final Network net = Network();

  final nameController = TextEditingController();
  final phoneController = TextEditingController();
  final passwordController = TextEditingController(text: "123456");
  final cityController = TextEditingController();
  final locationController = TextEditingController();
  final latitudeController = TextEditingController();
  final longitudeController = TextEditingController();

  bool saving = false;

  @override
  void dispose() {
    nameController.dispose();
    phoneController.dispose();
    passwordController.dispose();
    cityController.dispose();
    locationController.dispose();
    latitudeController.dispose();
    longitudeController.dispose();
    super.dispose();
  }

  Future<void> saveDriver() async {
    if (nameController.text.trim().isEmpty) {
      Get.snackbar("تنبيه", "اكتب اسم السائق");
      return;
    }

    if (phoneController.text.trim().isEmpty) {
      Get.snackbar("تنبيه", "اكتب رقم هاتف السائق");
      return;
    }

    setState(() => saving = true);

    try {
      await net.postMap(Links.createDriver, {
        "name": nameController.text.trim(),
        "phone": phoneController.text.trim(),
        "password": passwordController.text.trim().isEmpty
            ? "123456"
            : passwordController.text.trim(),
        "city": cityController.text.trim(),
        "location": locationController.text.trim(),
        "latitude": latitudeController.text.trim(),
        "longitude": longitudeController.text.trim(),
      });

      Get.snackbar("تم", "تمت إضافة السائق");
      Get.back(result: true);
    } catch (e) {
      Get.snackbar("خطأ", "فشل إضافة السائق: $e");
    } finally {
      if (mounted) setState(() => saving = false);
    }
  }

  Widget field(
    TextEditingController controller,
    String label, {
    TextInputType keyboardType = TextInputType.text,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: TextField(
        controller: controller,
        keyboardType: keyboardType,
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("إضافة سائق"),
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
        ),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            field(nameController, "اسم السائق"),
            field(phoneController, "رقم الهاتف", keyboardType: TextInputType.phone),
            field(passwordController, "كلمة المرور"),
            field(cityController, "المدينة"),
            field(locationController, "العنوان"),
            const Divider(height: 24),
            const Text(
              "موقع السائق على الخريطة - اختياري",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            field(latitudeController, "Latitude / خط العرض", keyboardType: TextInputType.number),
            field(longitudeController, "Longitude / خط الطول", keyboardType: TextInputType.number),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              onPressed: saving ? null : saveDriver,
              icon: const Icon(Icons.save),
              label: Text(saving ? "جاري الحفظ..." : "حفظ السائق"),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF1E9B4B),
                foregroundColor: Colors.white,
                minimumSize: const Size.fromHeight(52),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
