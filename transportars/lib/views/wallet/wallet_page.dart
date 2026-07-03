import 'package:flutter/material.dart';
import '../../services/links.dart';
import '../../services/network.dart';

class WalletPage extends StatefulWidget {
  const WalletPage({super.key});

  @override
  State<WalletPage> createState() => _WalletPageState();
}

class _WalletPageState extends State<WalletPage> {
  final net = Network();
  bool loading = true;
  int balance = 0;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() => loading = true);
    try {
      final data = await net.getMap(Links.wallet);
      balance = int.tryParse("${data['balance'] ?? 0}") ?? 0;
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(title: const Text("المحفظة")),
      body: Center(child: loading ? const CircularProgressIndicator() : Text("الرصيد: $balance IQD", style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold))),
    ));
  }
}
