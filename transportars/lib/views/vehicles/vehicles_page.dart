import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../models/vehicle.dart';
import '../../services/links.dart';
import '../../services/network.dart';
import 'add_vehicle_page.dart';

class VehiclesPage extends StatefulWidget {
  const VehiclesPage({super.key});

  @override
  State<VehiclesPage> createState() => _VehiclesPageState();
}

class _VehiclesPageState extends State<VehiclesPage> {
  final Network net = Network();

  bool loading = true;
  List<VehicleModel> vehicles = [];

  @override
  void initState() {
    super.initState();
    loadVehicles();
  }

  Future<void> loadVehicles() async {
    setState(() => loading = true);

    try {
      final list = await net.getList(Links.vehicles);

      vehicles = list
          .map((item) => VehicleModel.fromJson(Map<String, dynamic>.from(item)))
          .toList();
    } catch (e) {
      Get.snackbar("خطأ", "تعذر تحميل المركبات: $e");
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> openAddVehicle() async {
    final changed = await Get.to(() => const AddVehiclePage());

    if (changed == true) {
      loadVehicles();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("المركبات"),
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
          actions: [
            IconButton(
              onPressed: loadVehicles,
              icon: const Icon(Icons.refresh),
            ),
          ],
        ),
        floatingActionButton: FloatingActionButton.extended(
          onPressed: openAddVehicle,
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
          icon: const Icon(Icons.add),
          label: const Text("إضافة مركبة"),
        ),
        body: loading
            ? const Center(child: CircularProgressIndicator())
            : vehicles.isEmpty
                ? const Center(
                    child: Text(
                      "لا توجد مركبات حالياً\nاضغط إضافة مركبة",
                      textAlign: TextAlign.center,
                    ),
                  )
                : ListView.separated(
                    itemCount: vehicles.length,
                    separatorBuilder: (context, index) => const Divider(height: 1),
                    itemBuilder: (context, index) {
                      final v = vehicles[index];

                      return ListTile(
                        leading: const CircleAvatar(
                          backgroundColor: Color(0xFF1E9B4B),
                          child: Icon(Icons.local_shipping, color: Colors.white),
                        ),
                        title: Text(v.name),
                        trailing: const Icon(Icons.chevron_left),
                      );
                    },
                  ),
      ),
    );
  }
}
