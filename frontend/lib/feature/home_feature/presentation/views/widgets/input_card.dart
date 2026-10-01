import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_privacy_note.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_tap_row.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_text_area.dart';
import 'package:flutter/material.dart';

class InputCard extends StatelessWidget {
  // final List<String> tabs;
  // final int currentTab;
  // final TextEditingController controller;
  // final String placeholder;
  // final ValueChanged<int> onTabChanged;

  const InputCard({
    super.key,
    // required this.tabs,
    // required this.currentTab,
    // required this.controller,
    // required this.placeholder,
    // required this.onTabChanged,
  });

  @override
  Widget build(BuildContext context) {
    //final colors = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.all(16),

      decoration: BoxDecoration(
        color: AppColors.surfaceColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.surfaceColor.withOpacity(0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Analyze Content',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              letterSpacing: 0.5,
              color: AppColors.grayColor,
            ),
          ),

          BuildTapRow(),
          BuildTextArea(),
          SizedBox(height: responsiveHeight(context, 10)),
          BuildPrivacyNote(
            text: "We only analyze threats, not personal data ",
            color: Colors.greenAccent,
          ),
        ],
      ),
    );
  }
}
