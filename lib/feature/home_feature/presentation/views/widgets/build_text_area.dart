import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:flutter/material.dart';

class BuildTextArea extends StatelessWidget {
  const BuildTextArea({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    // done responsive
    double padding = screenWidth < 600 ? 16 : 24;
    double hintFontSize = screenWidth < 600 ? 14 : 16;

    return TextField(
      maxLines: 6,
      cursorColor: AppColors.grayColor,
      decoration: InputDecoration(
        hintText: "Paste SMS Message here ...",
        hintStyle: TextStyle(
          color: AppColors.gray2Color.withOpacity(0.30),
          fontSize: hintFontSize,
        ),
        filled: true,
        fillColor: AppColors.gray2Color,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(
            color: AppColors.primaryColor.withOpacity(0.07),
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(
            color: AppColors.primaryColor.withOpacity(0.07),
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(
            color: AppColors.primaryColor.withOpacity(0.07),
          ),
        ),
        contentPadding: EdgeInsets.all(padding),
      ),
    );
  }
}
