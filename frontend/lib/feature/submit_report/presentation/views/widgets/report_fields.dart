import 'package:cyper_shield_jo/core/constants/app_colors.dart' show AppColors;
import 'package:flutter/material.dart';

class ReportsFields extends StatelessWidget {
  const ReportsFields({
    super.key,
    required this.textFont,
    required this.hintText,
    this.controller,
    @Deprecated('No longer used — padding is handled internally')
    double textFieldPadding = 16,
  });

  final double textFont;
  final String hintText;
  final TextEditingController? controller;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      maxLines: 3,
      cursorColor: AppColors.grayColor,
      style: TextStyle(color: AppColors.whiteColor, fontSize: 13),
      decoration: InputDecoration(
        hintText: hintText,
        hintStyle: TextStyle(
          color: AppColors.grayColor,
          fontSize: textFont - 1,
        ),
        filled: true,
        fillColor: AppColors.backgroundColor,
        contentPadding: EdgeInsets.all(14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.grayColor),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.grayColor),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: AppColors.grayColor),
        ),
      ),
    );
  }
}
