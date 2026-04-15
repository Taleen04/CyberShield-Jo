import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/feature/submit_report/presentation/views/widgets/report_fields.dart';
import 'package:flutter/material.dart';

// ─── Shared input decoration helper ──────────────────────────────────────────
InputDecoration _csInputDecoration({required String hint}) {
  return InputDecoration(
    hintText: hint,
    hintStyle: TextStyle(color: AppColors.whiteColor, fontSize: 13),
    filled: true,
    fillColor: AppColors.backgroundColor,
    contentPadding: EdgeInsets.symmetric(horizontal: 14, vertical: 12),
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
  );
}

void submitReport(BuildContext context) {
  showDialog(
    context: context,
    barrierColor: Colors.black.withOpacity(0.72),
    builder: (context) => const _SubmitReportDialog(),
  );
}

class _SubmitReportDialog extends StatefulWidget {
  const _SubmitReportDialog();
  @override
  State<_SubmitReportDialog> createState() => _SubmitReportDialogState();
}

class _SubmitReportDialogState extends State<_SubmitReportDialog> {
  String? selectedType;
  bool isAnonymous = false;
  bool allowFollowUp = false;
  String location = "Jordan";
  bool submitted = false;

  final _pasteCtrl = TextEditingController();
  final _descCtrl = TextEditingController();

  @override
  void dispose() {
    _pasteCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  // ── Root build ───────────────────────────────────────────────────────────
  @override
  Widget build(BuildContext context) {
    final sw = MediaQuery.of(context).size.width;
    final double textFont = sw < 600 ? 14 : 16;
    final double titleFont = sw < 600 ? 16 : 20;

    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 500),
        child: Container(
          decoration: BoxDecoration(
            color: AppColors.backgroundColor,
            borderRadius: BorderRadius.circular(24),
            border: Border.all(color: AppColors.primaryColor.withOpacity(0.18)),
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildHeader(titleFont, textFont),
                Flexible(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(20),
                    child: submitted ? _buildSuccess() : _buildForm(textFont),
                  ),
                ),
                if (!submitted) _buildFooter(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // ── Header — replaces AlertDialog title ────────────────────────────────────
  Widget _buildHeader(double titleFont, double textFont) {
    return Container(
      padding: const EdgeInsets.fromLTRB(20, 20, 20, 16),
      decoration: BoxDecoration(
        color: AppColors.backgroundColor,
        border: Border(bottom: BorderSide(color: AppColors.whiteColor)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              // Shield badge
              Container(
                width: 42,
                height: 42,
                decoration: BoxDecoration(
                  color: AppColors.primaryColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(13),
                  border: Border.all(
                    color: AppColors.primaryColor.withOpacity(0.3),
                  ),
                ),
                child: Icon(
                  Icons.shield_outlined,
                  color: AppColors.primaryColor,
                  size: 22,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Report this threat",
                      style: TextStyle(
                        color: AppColors.whiteColor,
                        fontSize: titleFont,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      "Help us protect you and others by reporting any suspicious online activities.",
                      style: TextStyle(
                        color: AppColors.whiteColor,
                        fontSize: textFont - 3,
                      ),
                    ),
                  ],
                ),
              ),
              // Close button
              GestureDetector(
                onTap: () => Navigator.pop(context),
                child: Container(
                  width: 28,
                  height: 28,
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.06),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    Icons.close,
                    color: AppColors.whiteColor,
                    size: 14,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),

          // Progress bar (new addition)
        ],
      ),
    );
  }

  // ── Form — replaces AlertDialog content ────────────────────────────────────
  Widget _buildForm(double textFont) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Active threat indicator (new)
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: AppColors.redColor.withOpacity(0.12),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: AppColors.redColor.withOpacity(0.3)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 5,
                height: 5,
                decoration: BoxDecoration(
                  color: AppColors.redColor,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 6),
              Text(
                "Active threat detected",
                style: TextStyle(
                  color: AppColors.redColor,
                  fontSize: 10,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // ── TYPE —  ───────────────────────
        _FieldLabel(label: "Choose the type of threat"),
        const SizedBox(height: 7),
        DropdownButtonFormField<String>(
          value: selectedType,
          hint: Text(
            "Select type",
            style: TextStyle(color: AppColors.whiteColor, fontSize: 13),
          ),
          dropdownColor: AppColors.backgroundColor,
          style: TextStyle(color: AppColors.whiteColor, fontSize: 13),
          icon: Icon(
            Icons.keyboard_arrow_down,
            color: AppColors.primaryColor,
            size: 18,
          ),
          decoration: _csInputDecoration(hint: ""),
          items: const [
            DropdownMenuItem(value: "SMS Message", child: Text("SMS Message")),
            DropdownMenuItem(
              value: "Suspicious Link",
              child: Text("Suspicious Link"),
            ),
            DropdownMenuItem(
              value: "Suspicious Call",
              child: Text("Suspicious Call"),
            ),
          ],
          onChanged: (value) => setState(() => selectedType = value),
        ),
        const SizedBox(height: 16),

        // ── PASTE THREAT — was: ReportsFields(hintText: "Paste The Threat...") ──
        _FieldLabel(label: "Paste the threat"),
        const SizedBox(height: 7),
        ReportsFields(
          textFont: textFont,
          controller: _pasteCtrl,
          hintText: "Paste the suspicious message, link, or content here....",
        ),
        const SizedBox(height: 16),

        // ── DESCRIPTION — was: ReportsFields(hintText: "Describe what happened") ──
        _FieldLabel(label: "Description"),
        const SizedBox(height: 7),
        ReportsFields(
          textFont: textFont,
          controller: _descCtrl,
          hintText: "Describe what happened ....",
        ),
        const SizedBox(height: 16),

        const _CsDivider(),

        // ── LOCATION — was: plain Text + three RadioListTiles ────────────
        _FieldLabel(label: "Location"),
        const SizedBox(height: 10),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children:
              {
                    "Jordan": "Inside Jordan",
                    "Outside": "Outside Jordan",
                    "Unknown": "Unknown",
                  }.entries
                  .map(
                    (e) => GestureDetector(
                      onTap: () => setState(() => location = e.key),
                      child: _RadioChip(
                        label: e.value,
                        active: location == e.key,
                      ),
                    ),
                  )
                  .toList(),
        ),
        const SizedBox(height: 16),

        const _CsDivider(),

        // ── PRIVACY — was: plain Text + two CheckboxListTiles ─────────────
        _FieldLabel(label: "Privacy Options"),
        const SizedBox(height: 4),
        _CsCheckRow(
          label: "Submit anonymously",
          value: isAnonymous,
          onChanged: (v) => setState(() => isAnonymous = v),
        ),
        _CsCheckRow(
          label: "Allow follow-up contact",
          value: allowFollowUp,
          onChanged: (v) => setState(() => allowFollowUp = v),
          last: true,
        ),
        const SizedBox(height: 4),
      ],
    );
  }

  // ── Success view — replaces the second showDialog / AlertDialog ─────────────
  Widget _buildSuccess() {
    return Column(
      children: [
        const SizedBox(height: 16),
        Container(
          width: 70,
          height: 70,
          decoration: BoxDecoration(
            color: AppColors.primaryColor.withOpacity(0.15),
            shape: BoxShape.circle,
            border: Border.all(color: AppColors.primaryColor, width: 2),
          ),
          child: Icon(Icons.check, color: AppColors.primaryColor, size: 30),
        ),
        const SizedBox(height: 18),
        Text(
          "Report Submitted",
          style: TextStyle(
            color: AppColors.whiteColor,
            fontSize: 17,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          "Thank you for helping protect Jordan's digital community.\nOur security team will review your report shortly.",
          textAlign: TextAlign.center,
          style: TextStyle(
            color: AppColors.whiteColor,
            fontSize: 12,
            height: 1.6,
          ),
        ),
        const SizedBox(height: 16),
        // Case ID — was plain Text("Case ID: #CSJ-10234")
        Container(
          padding: EdgeInsets.symmetric(horizontal: 14, vertical: 5),
          decoration: BoxDecoration(
            color: AppColors.primaryColor.withOpacity(0.12),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: AppColors.primaryColor.withOpacity(0.25)),
          ),
          child: Text(
            "Case ID: #CSJ-10234",
            style: TextStyle(
              color: AppColors.primaryColor,
              fontSize: 11,
              fontFamily: 'monospace',
            ),
          ),
        ),
        const SizedBox(height: 18),
        // Risk badge — was plain Container with Colors.orange
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "Risk Level: ",
              style: TextStyle(color: AppColors.whiteColor, fontSize: 12),
            ),
            Container(
              padding: EdgeInsets.symmetric(horizontal: 14, vertical: 5),
              decoration: BoxDecoration(
                color: AppColors.orangeColor.withOpacity(0.12),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: AppColors.orangeColor.withOpacity(0.3),
                ),
              ),
              child: Text(
                "Medium ⚠️",
                style: TextStyle(
                  color: AppColors.orangeColor,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 22),
        // Done button — was TextButton("Done")
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: () => Navigator.pop(context),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: AppColors.grayColor),
              ),
              elevation: 0,
            ),
            child: const Text(
              "Done",
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
            ),
          ),
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  // ── Footer — replaces AlertDialog actions ──────────────────────────────────
  Widget _buildFooter() {
    return Container(
      padding: EdgeInsets.fromLTRB(20, 14, 20, 10),
      decoration: BoxDecoration(
        color: AppColors.backgroundColor,
        border: Border(top: BorderSide(color: AppColors.primaryColor)),
      ),
      child: Row(
        children: [
          // Cancel — was TextButton with AppColors.redColor
          OutlinedButton(
            onPressed: () => Navigator.pop(context),
            style: OutlinedButton.styleFrom(
              foregroundColor: AppColors.redColor,
              side: BorderSide(color: AppColors.redColor),
              backgroundColor: AppColors.redColor.withOpacity(0.12),
              padding: EdgeInsets.symmetric(horizontal: 18, vertical: 11),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: const Text(
              "Cancel",
              style: TextStyle(fontSize: 13, fontWeight: FontWeight.w500),
            ),
          ),
          const SizedBox(width: 10),
          // Submit — was ElevatedButton with AppColors.whiteColor text
          Expanded(
            child: ElevatedButton.icon(
              onPressed: () => setState(() => submitted = true),
              icon: const Icon(
                Icons.shield_outlined,
                size: 16,
                color: Colors.white,
              ),
              label: const Text(
                "Submit Report 🚨",
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: Colors.white,
                ),
              ),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                  side: BorderSide(color: AppColors.grayColor),
                ),
                elevation: 0,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ─── Reusable widgets ─────────────────────────────────────────────────────────

class _FieldLabel extends StatelessWidget {
  final String label;
  const _FieldLabel({required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 5,
          height: 5,
          decoration: BoxDecoration(
            color: AppColors.primaryColor,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 6),
        Text(
          label.toUpperCase(),
          style: TextStyle(
            color: AppColors.whiteColor,
            fontSize: 11,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.5,
          ),
        ),
      ],
    );
  }
}

class _CsDivider extends StatelessWidget {
  const _CsDivider();
  @override
  Widget build(BuildContext context) => Container(
    height: 1,
    margin: const EdgeInsets.only(bottom: 16),
    color: AppColors.grayColor,
  );
}

class _RadioChip extends StatelessWidget {
  final String label;
  final bool active;
  const _RadioChip({required this.label, required this.active});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 150),
      padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 8),
      decoration: BoxDecoration(
        color: active
            ? AppColors.primaryColor.withOpacity(0.12)
            : AppColors.backgroundColor,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: active ? AppColors.primaryColor : AppColors.whiteColor,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          AnimatedContainer(
            duration: const Duration(milliseconds: 150),
            width: 13,
            height: 13,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: active ? AppColors.primaryColor : Colors.transparent,
              border: Border.all(
                color: active ? AppColors.primaryColor : AppColors.whiteColor,
                width: 2,
              ),
            ),
            child: active
                ? Center(
                    child: CircleAvatar(
                      radius: 2,
                      backgroundColor: Colors.white,
                    ),
                  )
                : null,
          ),
          const SizedBox(width: 7),
          Text(
            label,
            style: TextStyle(
              color: active ? const Color(0xFFA0BAFF) : AppColors.whiteColor,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }
}

class _CsCheckRow extends StatelessWidget {
  final String label;
  final bool value;
  final ValueChanged<bool> onChanged;
  final bool last;
  const _CsCheckRow({
    required this.label,
    required this.value,
    required this.onChanged,
    this.last = false,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => onChanged(!value),
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          border: last
              ? null
              : Border(
                  bottom: BorderSide(color: AppColors.whiteColor, width: 0.5),
                ),
        ),
        child: Row(
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 150),
              width: 18,
              height: 18,
              decoration: BoxDecoration(
                color: value ? AppColors.primaryColor : Colors.transparent,
                borderRadius: BorderRadius.circular(5),
                border: Border.all(
                  color: value ? AppColors.primaryColor : AppColors.whiteColor,
                  width: 1.5,
                ),
              ),
              child: value
                  ? Icon(Icons.check, size: 11, color: Colors.white)
                  : null,
            ),
            const SizedBox(width: 10),
            Text(
              label,
              style: const TextStyle(color: Color(0xFF8A9FCC), fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }
}
