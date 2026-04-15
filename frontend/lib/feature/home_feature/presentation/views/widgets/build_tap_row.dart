import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:flutter/material.dart';

class BuildTapRow extends StatelessWidget {
  const BuildTapRow({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    // done responsive
    double containerPadding = screenWidth < 600 ? 16 : 30;
    double rowVerticalPadding = screenWidth < 600 ? 6 : 9;
    double fontSize = screenWidth < 600 ? 14 : 16;

    return Container(
      decoration: BoxDecoration(
        color: AppColors.surfaceColor.withOpacity(0.06),
      ),
      child: Padding(
        padding: EdgeInsets.all(containerPadding),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: EdgeInsets.symmetric(vertical: rowVerticalPadding),
          decoration: BoxDecoration(
            color: AppColors.seconderyColor.withOpacity(0.07),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text(
                "SMS",
                style: TextStyle(
                  color: AppColors.primaryColor,
                  fontSize: fontSize,
                ),
              ),
              Text("Phone", style: TextStyle(fontSize: fontSize)),
              Text("Link", style: TextStyle(fontSize: fontSize)),
            ],
          ),
        ),
      ),
    );
  }
}
