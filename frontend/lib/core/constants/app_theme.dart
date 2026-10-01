import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:flutter/material.dart';

class AppTheme {
  static final dark = ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: AppColors.backgroundColor,
    colorScheme: ColorScheme.dark(
      primary: AppColors.primaryColor,
      secondary: AppColors.seconderyColor,
      surface: AppColors.surfaceColor,
      error: const Color(0xFFE85D5D),
    ),
    fontFamily: 'Inter',
    useMaterial3: true,
  );
}
