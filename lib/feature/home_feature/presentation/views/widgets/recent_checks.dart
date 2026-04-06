import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:flutter/material.dart';

class RecentChecks extends StatelessWidget {
  const RecentChecks({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    double horizontalMargin = screenWidth < 600 ? 16 : 20;
    double containerPadding = screenWidth < 600 ? 12 : 16;
    double titleFont = screenWidth < 600 ? 16 : 18;
    double textFont = screenWidth < 600 ? 14 : 18;
    double spacingHeight = screenWidth < 600 ? 12 : 16;
    double bottomSpacing = screenWidth < 600 ? 20 : 60;

    return Container(
      padding: EdgeInsets.all(containerPadding),
      margin: EdgeInsets.symmetric(horizontal: horizontalMargin),
      decoration: BoxDecoration(
        color: AppColors.surfaceColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.surfaceColor.withOpacity(0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Recent Checks',
            style: TextStyle(
              fontSize: titleFont,
              fontWeight: FontWeight.w600,
              letterSpacing: 0.5,
              color: AppColors.grayColor,
            ),
          ),
          SizedBox(height: spacingHeight),
          Row(
            children: [
              Icon(Icons.link, color: AppColors.grayColor),
              SizedBox(width: 12),

              /// Expanded عشان النص لا يكسر الشاشة
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'http://www.google.com',
                      style: TextStyle(
                        fontSize: textFont,
                        fontWeight: FontWeight.w600,
                        letterSpacing: 0.5,
                        color: AppColors.whiteColor,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      "12/12/2022",
                      style: TextStyle(
                        color: AppColors.grayColor.withOpacity(0.5),
                        fontSize: textFont - 4,
                      ),
                    ),
                  ],
                ),
              ),

              SizedBox(width: 12),
              Text(
                "Safe",
                style: TextStyle(
                  color: AppColors.greenColor,
                  fontSize: textFont,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          SizedBox(height: bottomSpacing),
        ],
      ),
    );
  }
}
