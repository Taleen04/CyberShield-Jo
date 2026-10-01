import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:flutter/material.dart';

class PercentageCircle extends StatelessWidget {
  final double percentage;

  const PercentageCircle({super.key, required this.percentage});

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: [
        SizedBox(
          width: responsiveWidth(context, 80),
          height: responsiveHeight(context, 80),
          child: CircularProgressIndicator(
            value: percentage,
            strokeWidth: 10,
            backgroundColor: AppColors.redColor.withOpacity(0.06),
            valueColor: AlwaysStoppedAnimation<Color>(AppColors.redColor),
          ),
        ),
        Text(
          "${(percentage * 100).toInt()}%",
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: AppColors.redColor,
          ),
        ),
      ],
    );
  }
}
