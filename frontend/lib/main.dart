import 'package:cyper_shield_jo/core/constants/app_theme.dart';
import 'package:cyper_shield_jo/core/widgets/bottom_nav_bar.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cyper Shield Demo',
      debugShowCheckedModeBanner: false,
      darkTheme: AppTheme.dark,
      //theme:, if we add light theme
      home: const BottomNavBar(),
    );
  }
}
