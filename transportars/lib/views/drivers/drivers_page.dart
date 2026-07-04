import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../models/driver.dart';
import '../../services/links.dart';
import '../../services/network.dart';
import 'add_driver_page.dart';

class DriversPage extends StatefulWidget {
  const DriversPage({super.key});

  @override
  State<DriversPage> createState() => _DriversPageState();
}

class _DriversPageState extends State<DriversPage> {
  final Network net = Network();

  bool loading = true;
  List<DriverModel> drivers = [];

  @override
  void initState() {
    super.initState();
    loadDrivers();
  }

  Future<void> loadDrivers() async {
    setState(() => loading = true);

    try {
      final list = await net.getList(Links.drivers);

      drivers = list
          .map((item) => DriverModel.fromJson(Map<String, dynamic>.from(item)))
          .toList();
    } catch (e) {
      Get.snackbar("خطأ", "تعذر تحميل السائقين: $e");
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> openAddDriver() async {
    final changed = await Get.to(() => const AddDriverPage());

    if (changed == true) {
      loadDrivers();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("السائقين"),
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
          actions: [
            IconButton(
              onPressed: loadDrivers,
              icon: const Icon(Icons.refresh),
            ),
          ],
        ),
        floatingActionButton: FloatingActionButton.extended(
          onPressed: openAddDriver,
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
          icon: const Icon(Icons.add),
          label: const Text("إضافة سائق"),
        ),
        body: loading
            ? const Center(child: CircularProgressIndicator())
            : drivers.isEmpty
                ? const Center(
                    child: Text(
                      "لا يوجد سائقون حالياً\nاضغط إضافة سائق",
                      textAlign: TextAlign.center,
                    ),
                  )
                : ListView.separated(
                    itemCount: drivers.length,
                    separatorBuilder: (context, index) => const Divider(height: 1),
                    itemBuilder: (context, index) {
                      final d = drivers[index];

                      return ListTile(
                        leading: const CircleAvatar(
                          backgroundColor: Color(0xFF1E9B4B),
                          child: Icon(Icons.person, color: Colors.white),
                        ),
                        title: Text(d.name),
                        subtitle: Text(d.phone ?? ""),
                        trailing: const Icon(Icons.chevron_left),
                      );
                    },
                  ),
      ),
    );
  }
}
