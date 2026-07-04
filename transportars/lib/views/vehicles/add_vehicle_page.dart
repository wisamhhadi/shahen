import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../services/links.dart';
import '../../services/network.dart';

class AddVehiclePage extends StatefulWidget {
  const AddVehiclePage({super.key});

  @override
  State<AddVehiclePage> createState() => _AddVehiclePageState();
}

class _AddVehiclePageState extends State<AddVehiclePage> {
  final Network net = Network();

  final nameController = TextEditingController();
  final plateController = TextEditingController();
  final modelController = TextEditingController();
  final colorController = TextEditingController();
  final noteController = TextEditingController();

  bool saving = false;

  @override
  void dispose() {
    nameController.dispose();
    plateController.dispose();
    modelController.dispose();
    colorController.dispose();
    noteController.dispose();
    super.dispose();
  }

  Future<void> saveVehicle() async {
    if (nameController.text.trim().isEmpty && plateController.text.trim().isEmpty) {
      Get.snackbar("تنبيه", "اكتب اسم المركبة أو رقم اللوحة");
      return;
    }

    setState(() => saving = true);

    try {
      await net.postMap(Links.createVehicle, {
        "name": nameController.text.trim(),
        "plate": plateController.text.trim(),
        "model": modelController.text.trim(),
        "color": colorController.text.trim(),
        "note": noteController.text.trim(),
      });

      Get.snackbar("تم", "تمت إضافة المركبة");
      Get.back(result: true);
    } catch (e) {
      Get.snackbar("خطأ", "فشل إضافة المركبة: $e");
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
          title: const Text("إضافة مركبة"),
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
        ),
        body: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            field(nameController, "اسم المركبة / نوع المركبة"),
            field(plateController, "رقم اللوحة"),
            field(modelController, "الموديل"),
            field(colorController, "اللون"),
            field(noteController, "ملاحظات"),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              onPressed: saving ? null : saveVehicle,
              icon: const Icon(Icons.save),
              label: Text(saving ? "جاري الحفظ..." : "حفظ المركبة"),
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
