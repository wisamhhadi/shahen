import 'package:flutter/material.dart';
import '../../models/driver.dart';
import '../../services/links.dart';
import '../../services/network.dart';

class DriversPage extends StatefulWidget {
  const DriversPage({super.key});

  @override
  State<DriversPage> createState() => _DriversPageState();
}

class _DriversPageState extends State<DriversPage> {
  final net = Network();
  bool loading = true;
  List<DriverModel> drivers = [];

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() => loading = true);
    try {
      final list = await net.getList(Links.drivers);
      drivers = list.map((e) => DriverModel.fromJson(Map<String, dynamic>.from(e))).toList();
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(title: const Text("السائقين")),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.separated(
              itemCount: drivers.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final d = drivers[index];
                return ListTile(
                  leading: const CircleAvatar(child: Icon(Icons.person)),
                  title: Text(d.name),
                  subtitle: Text("${d.phone ?? ''}\nالمركبة: ${d.carNumber ?? '-'}"),
                  isThreeLine: true,
                  trailing: const Row(mainAxisSize: MainAxisSize.min, children: [
                    Icon(Icons.star, color: Colors.amber),
                    SizedBox(width: 4),
                    Text("5.0"),
                  ]),
                );
              },
            ),
    ));
  }
}
