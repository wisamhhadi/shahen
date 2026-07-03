import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

import 'services/storage.dart';
import 'views/auth/login.dart';
import 'views/home/home.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await GetStorage.init();

  runApp(GetMaterialApp(
    title: 'شحنكو - الناقلين',
    debugShowCheckedModeBanner: false,
    locale: const Locale('ar', 'IQ'),
    theme: ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1E9B4B)),
      scaffoldBackgroundColor: const Color(0xFFF4F7F5),
    ),
    initialRoute: AppStorage.token == null ? '/login' : '/home',
    getPages: [
      GetPage(name: '/login', page: () => const LoginPage()),
      GetPage(name: '/home', page: () => const HomePage()),
    ],
  ));
}
