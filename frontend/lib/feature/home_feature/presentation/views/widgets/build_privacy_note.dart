import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:flutter/material.dart';

class BuildPrivacyNote extends StatelessWidget {
  const BuildPrivacyNote({super.key, required this.text, required this.color});

  final String text;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          height: responsiveHeight(context, 10),
          width: responsiveWidth(context, 10),
          decoration: BoxDecoration(shape: BoxShape.circle, color: color),
        ),
        SizedBox(width: responsiveWidth(context, 10)),
        Text(text, style: TextStyle(color: AppColors.grayColor, fontSize: 12)),
      ],
    );
  }
}
