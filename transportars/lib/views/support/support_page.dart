import 'package:flutter/material.dart';

class SupportPage extends StatelessWidget {
  const SupportPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Directionality(textDirection: TextDirection.rtl, child: Scaffold(
      appBar: AppBar(title: Text("الدعم الفني")),
      body: Center(child: Text("صفحة الدعم الفني - V1")),
    ));
  }
}
