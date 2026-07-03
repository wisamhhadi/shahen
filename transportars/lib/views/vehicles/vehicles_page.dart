import 'package:flutter/material.dart';
import '../../models/vehicle.dart';
import '../../services/links.dart';
import '../../services/network.dart';

class VehiclesPage extends StatefulWidget {
  const VehiclesPage({super.key});

  @override
  State<VehiclesPage> createState() => _VehiclesPageState();
}

class _VehiclesPageState extends State<VehiclesPage> {
  final net = Network();
  bool loading = true;
  List<VehicleModel> vehicles = [];

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() => loading = true);
    try {
      final list = await net.getList(Links.vehicles);
      vehicles = list.map((e) => VehicleModel.fromJson(Map<String, dynamic>.from(e))).toList();
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(title: const Text("المركبات")),
      floatingActionButton: FloatingActionButton(onPressed: () {}, child: const Icon(Icons.add)),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.separated(
              itemCount: vehicles.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final v = vehicles[index];
                return ListTile(
                  leading: const CircleAvatar(child: Icon(Icons.local_shipping)),
                  title: Text(v.name),
                  subtitle: Text("السائق: ${v.captainName ?? '-'}"),
                );
              },
            ),
    ));
  }
}
