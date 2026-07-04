import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../models/stats.dart';
import '../../models/transporter.dart';
import '../../services/links.dart';
import '../../services/network.dart';
import '../../services/storage.dart';
import '../../widgets/stat_card.dart';
import '../drivers/drivers_page.dart';
import '../vehicles/vehicles_page.dart';
import '../orders/orders_page.dart';
import '../support/support_page.dart';
import 'map_screen.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final Network net = Network();

  bool loading = true;
  Transporter? transporter;
  Stats? stats;

  @override
  void initState() {
    super.initState();
    loadDashboard();
  }

  Future<void> loadDashboard() async {
    setState(() => loading = true);

    try {
      final data = await net.getMap(Links.me);

      transporter = Transporter.fromJson(
        Map<String, dynamic>.from(data['transporter'] ?? {}),
      );

      stats = Stats.fromJson(
        Map<String, dynamic>.from(data['stats'] ?? {}),
      );
    } catch (e) {
      Get.snackbar(
        "خطأ",
        "تعذر تحميل بيانات الناقل: $e",
        snackPosition: SnackPosition.BOTTOM,
      );
    } finally {
      if (mounted) {
        setState(() => loading = false);
      }
    }
  }

  Future<void> logout() async {
    await AppStorage.clear();
    Get.offAllNamed('/login');
  }

  @override
  Widget build(BuildContext context) {
    final Stats? s = stats;

    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        endDrawer: Drawer(
          child: SafeArea(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                Container(
                  padding: const EdgeInsets.all(20),
                  color: const Color(0xFF1E9B4B),
                  child: Column(
                    children: [
                      const CircleAvatar(
                        radius: 35,
                        backgroundColor: Colors.white,
                        child: Icon(
                          Icons.local_shipping,
                          color: Color(0xFF1E9B4B),
                          size: 38,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        transporter?.name ?? "الناقل",
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        transporter?.phone ?? "",
                        style: const TextStyle(color: Colors.white70),
                      ),
                    ],
                  ),
                ),
                ListTile(
                  leading: const Icon(Icons.person),
                  title: const Text("حسابي"),
                  onTap: () {},
                ),
                ListTile(
                  leading: const Icon(Icons.local_shipping),
                  title: const Text("المركبات"),
                  onTap: () => Get.to(() => const VehiclesPage()),
                ),
                ListTile(
                  leading: const Icon(Icons.groups),
                  title: const Text("السائقين"),
                  onTap: () => Get.to(() => const DriversPage()),
                ),
                ListTile(
                  leading: const Icon(Icons.inventory_2),
                  title: const Text("الطلبات"),
                  onTap: () => Get.to(() => const OrdersPage()),
                ),
                ListTile(
                  leading: const Icon(Icons.support_agent),
                  title: const Text("الدعم الفني"),
                  onTap: () => Get.to(() => const SupportPage()),
                ),
                const Divider(),
                ListTile(
                  leading: const Icon(Icons.logout, color: Colors.red),
                  title: const Text("تسجيل خروج"),
                  onTap: logout,
                ),
              ],
            ),
          ),
        ),
        appBar: AppBar(
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
          centerTitle: true,
          title: Text(transporter?.name ?? "لوحة الناقل"),
          leading: IconButton(
            onPressed: loadDashboard,
            icon: const Icon(Icons.refresh),
          ),
        ),
        body: loading
            ? const Center(child: CircularProgressIndicator())
            : RefreshIndicator(
                onRefresh: loadDashboard,
                child: ListView(
                  padding: const EdgeInsets.all(14),
                  children: [
                    SizedBox(
                      height: 260,
                      child: TransporterMapScreen(
                        transporter: transporter,
                      ),
                    ),
                    const SizedBox(height: 14),
                    GridView.count(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      crossAxisCount: 2,
                      childAspectRatio: 1.25,
                      crossAxisSpacing: 12,
                      mainAxisSpacing: 12,
                      children: [
                        StatCard(
                          title: "عدد السائقين",
                          value: "${s?.drivers ?? 0}",
                          icon: Icons.groups,
                          onTap: () => Get.to(() => const DriversPage()),
                        ),
                        StatCard(
                          title: "عدد المركبات",
                          value: "${s?.vehicles ?? 0}",
                          icon: Icons.local_shipping,
                          onTap: () => Get.to(() => const VehiclesPage()),
                        ),
                        StatCard(
                          title: "إجمالي الشحنات",
                          value: "${s?.orders ?? 0}",
                          icon: Icons.inventory_2,
                          onTap: () => Get.to(() => const OrdersPage()),
                        ),
                        StatCard(
                          title: "مركبات ملتزمة",
                          value: "${s?.committed ?? 0}",
                          icon: Icons.task_alt,
                        ),
                        StatCard(
                          title: "رحلات مكتملة",
                          value: "${s?.activeOrders ?? 0}",
                          icon: Icons.done_all,
                        ),
                        StatCard(
                          title: "سائقون بحاجة مساعدة",
                          value: "${s?.help ?? 0}",
                          icon: Icons.support_agent,
                        ),
                        StatCard(
                          title: "مركبات قيد الصيانة",
                          value: "${s?.maintenance ?? 0}",
                          icon: Icons.build,
                        ),
                        StatCard(
                          title: "سائقون متوقفون",
                          value: "${s?.stopped ?? 0}",
                          icon: Icons.timer_off,
                        ),
                      ],
                    ),
                    const SizedBox(height: 18),
                    ElevatedButton.icon(
                      onPressed: () => Get.to(() => const OrdersPage()),
                      icon: const Icon(Icons.assignment),
                      label: const Text("إدارة الطلبات وتوزيعها"),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF1E9B4B),
                        foregroundColor: Colors.white,
                        minimumSize: const Size.fromHeight(52),
                      ),
                    ),
                  ],
                ),
              ),
      ),
    );
  }
}
