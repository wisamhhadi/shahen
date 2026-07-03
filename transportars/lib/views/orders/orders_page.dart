import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../models/order.dart';
import '../../services/links.dart';
import '../../services/network.dart';
import 'assign_order_page.dart';

class OrdersPage extends StatefulWidget {
  const OrdersPage({super.key});

  @override
  State<OrdersPage> createState() => _OrdersPageState();
}

class _OrdersPageState extends State<OrdersPage> {
  final net = Network();
  bool loading = true;
  List<TransportOrder> orders = [];

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() => loading = true);
    try {
      final list = await net.getList(Links.orders);
      orders = list.map((e) => TransportOrder.fromJson(Map<String, dynamic>.from(e))).toList();
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(title: const Text("الطلبات")),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.separated(
              itemCount: orders.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final o = orders[index];
                return ListTile(
                  leading: const CircleAvatar(child: Icon(Icons.inventory_2)),
                  title: Text(o.title),
                  subtitle: Text("من: ${o.fromName ?? '-'}  ←  إلى: ${o.toName ?? '-'}\nالسائق: ${o.captainName ?? '-'}"),
                  isThreeLine: true,
                  trailing: ElevatedButton(onPressed: () => Get.to(() => AssignOrderPage(order: o)), child: const Text("توزيع")),
                );
              },
            ),
    ));
  }
}
