import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../models/driver.dart';
import '../../models/order.dart';
import '../../models/vehicle.dart';
import '../../services/links.dart';
import '../../services/network.dart';

class AssignOrderPage extends StatefulWidget {
  final TransportOrder order;
  const AssignOrderPage({super.key, required this.order});

  @override
  State<AssignOrderPage> createState() => _AssignOrderPageState();
}

class _AssignOrderPageState extends State<AssignOrderPage> {
  final net = Network();
  bool loading = true;
  bool saving = false;
  List<DriverModel> drivers = [];
  List<VehicleModel> vehicles = [];
  DriverModel? selectedDriver;
  VehicleModel? selectedVehicle;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() => loading = true);
    try {
      final d = await net.getList(Links.drivers);
      final v = await net.getList(Links.vehicles);
      drivers = d.map((e) => DriverModel.fromJson(Map<String, dynamic>.from(e))).toList();
      vehicles = v.map((e) => VehicleModel.fromJson(Map<String, dynamic>.from(e))).toList();
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> assign() async {
    if (selectedDriver == null) {
      Get.snackbar("تنبيه", "اختر السائق أولاً");
      return;
    }

    setState(() => saving = true);
    try {
      await net.postMap(Links.assignOrder(widget.order.id), {
        "driver_id": selectedDriver!.id,
        if (selectedVehicle != null) "vehicle_id": selectedVehicle!.id,
      });
      Get.snackbar("تم", "تم توزيع الطلب");
      Get.back();
    } catch (e) {
      Get.snackbar("خطأ", "فشل توزيع الطلب: $e");
    } finally {
      if (mounted) setState(() => saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(title: Text("توزيع الطلب #${widget.order.id}")),
      body: loading ? const Center(child: CircularProgressIndicator()) : ListView(padding: const EdgeInsets.all(16), children: [
        Text(widget.order.title, style: const TextStyle(fontSize: 21, fontWeight: FontWeight.bold)),
        const SizedBox(height: 18),
        DropdownButtonFormField<DriverModel>(
          value: selectedDriver,
          decoration: const InputDecoration(labelText: "السائق", border: OutlineInputBorder()),
          items: drivers.map((d) => DropdownMenuItem(value: d, child: Text(d.name))).toList(),
          onChanged: (v) => setState(() => selectedDriver = v),
        ),
        const SizedBox(height: 12),
        DropdownButtonFormField<VehicleModel>(
          value: selectedVehicle,
          decoration: const InputDecoration(labelText: "المركبة", border: OutlineInputBorder()),
          items: vehicles.map((v) => DropdownMenuItem(value: v, child: Text(v.name))).toList(),
          onChanged: (v) => setState(() => selectedVehicle = v),
        ),
        const SizedBox(height: 20),
        ElevatedButton.icon(onPressed: saving ? null : assign, icon: const Icon(Icons.check), label: Text(saving ? "جاري الحفظ..." : "تأكيد التوزيع")),
      ]),
    ));
  }
}
