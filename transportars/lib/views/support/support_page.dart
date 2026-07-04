import 'package:flutter/material.dart';

class SupportPage extends StatelessWidget {
  const SupportPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("الدعم الفني"),
          backgroundColor: const Color(0xFF1E9B4B),
          foregroundColor: Colors.white,
          centerTitle: true,
        ),
        body: const Center(
          child: Text("صفحة الدعم الفني - V1", style: TextStyle(fontSize: 18)),
        ),
      ),
    );
  }
}
