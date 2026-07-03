import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../models/stats.dart';
import '../../models/transporter.dart';
import '../../services/links.dart';
import '../../services/network.dart';
import '../../services/storage.dart';
import '../../widgets/stat_card.dart';
import '../drivers/drivers_page.dart';
import '../orders/orders_page.dart';
import '../vehicles/vehicles_page.dart';
import '../wallet/wallet_page.dart';
import '../support/support_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final net = Network();
  bool loading = true;
  Transporter? transporter;
  TransporterStats? stats;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() => loading = true);

    try {
      final data = await net.getMap(Links.me);
      transporter = Transporter.fromJson(Map<String, dynamic>.from(data["transporter"] ?? {}));
      stats = TransporterStats.fromJson(Map<String, dynamic>.from(data["stats"] ?? {}));
    } catch (e) {
      Get.snackbar("خطأ", "تعذر تحميل لوحة الناقل: $e");
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> logout() async {
    try {
      await net.postMap(Links.logout, {});
    } catch (_) {}
    await AppStorage.clear();
    Get.offAllNamed('/login');
  }

  @override
  Widget build(BuildContext context) {
    final s = stats;

    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(
        title: Text(transporter?.name ?? "لوحة الناقل"),
        centerTitle: true,
        backgroundColor: const Color(0xFF1E9B4B),
        foregroundColor: Colors.white,
        actions: [
          IconButton(onPressed: load, icon: const Icon(Icons.refresh)),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF1E9B4B)),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                CircleAvatar(radius: 32, backgroundColor: Colors.white, child: Icon(Icons.local_shipping, color: Color(0xFF1E9B4B), size: 34)),
                SizedBox(height: 10),
                Text("شحنكو - الناقلين", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 19)),
              ]),
            ),
            ListTile(leading: const Icon(Icons.home), title: const Text("الرئيسية"), onTap: () => Get.back()),
            ListTile(leading: const Icon(Icons.groups), title: const Text("السائقين"), onTap: () => Get.to(() => const DriversPage())),
            ListTile(leading: const Icon(Icons.local_shipping), title: const Text("المركبات"), onTap: () => Get.to(() => const VehiclesPage())),
            ListTile(leading: const Icon(Icons.inventory_2), title: const Text("الطلبات"), onTap: () => Get.to(() => const OrdersPage())),
            ListTile(leading: const Icon(Icons.account_balance_wallet), title: const Text("المحفظة"), onTap: () => Get.to(() => const WalletPage())),
            ListTile(leading: const Icon(Icons.support_agent), title: const Text("الدعم الفني"), onTap: () => Get.to(() => const SupportPage())),
            ListTile(leading: const Icon(Icons.logout), title: const Text("تسجيل خروج"), onTap: logout),
          ],
        ),
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: load,
              child: ListView(padding: const EdgeInsets.all(14), children: [
                Container(
                  height: 210,
                  decoration: BoxDecoration(color: const Color(0xFFEAF5EE), borderRadius: BorderRadius.circular(22)),
                  child: const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                    Icon(Icons.map, size: 72, color: Color(0xFF1E9B4B)),
                    SizedBox(height: 8),
                    Text("خريطة السائقين والرحلات", style: TextStyle(fontWeight: FontWeight.bold)),
                  ])),
                ),
                const SizedBox(height: 14),
                GridView.count(
                  crossAxisCount: 2,
                  childAspectRatio: 1.35,
                  mainAxisSpacing: 12,
                  crossAxisSpacing: 12,
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  children: [
                    StatCard(title: "عدد السائقين", value: "${s?.driversCount ?? 0}", icon: Icons.groups, onTap: () => Get.to(() => const DriversPage())),
                    StatCard(title: "عدد المركبات", value: "${s?.vehiclesCount ?? 0}", icon: Icons.local_shipping, onTap: () => Get.to(() => const VehiclesPage())),
                    StatCard(title: "إجمالي الشحنات", value: "${s?.ordersCount ?? 0}", icon: Icons.inventory_2, onTap: () => Get.to(() => const OrdersPage())),
                    StatCard(title: "مركبات ملتزمة", value: "${s?.committedVehiclesCount ?? 0}", icon: Icons.task_alt),
                    StatCard(title: "رحلات مكتملة", value: "${s?.completedOrdersCount ?? 0}", icon: Icons.done_all),
                    StatCard(title: "رحلات مرفوضة", value: "${s?.rejectedOrdersCount ?? 0}", icon: Icons.cancel, color: Colors.redAccent),
                    StatCard(title: "سائقون بحاجة مساعدة", value: "${s?.driversNeedHelpCount ?? 0}", icon: Icons.support_agent, color: Colors.orange),
                    StatCard(title: "مركبات قيد الصيانة", value: "${s?.maintenanceVehiclesCount ?? 0}", icon: Icons.build, color: Colors.blueGrey),
                  ],
                ),
              ]),
            ),
    ));
  }
}
