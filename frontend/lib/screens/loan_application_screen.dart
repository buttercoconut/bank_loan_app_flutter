import 'package:flutter/material.dart';
import '../widgets/custom_button.dart';
import '../services/loan_api_service.dart';

class LoanApplicationScreen extends StatefulWidget {
  const LoanApplicationScreen({Key? key}) : super(key: key);

  @override
  State<LoanApplicationScreen> createState() => _LoanApplicationScreenState();
}

class _LoanApplicationScreenState extends State<LoanApplicationScreen> {
  final _formKey = GlobalKey<FormState>();
  final _amountController = TextEditingController();
  final _termController = TextEditingController();
  bool _isSubmitting = false;
  String? _error;

  @override
  void dispose() {
    _amountController.dispose();
    _termController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _isSubmitting = true;
      _error = null;
    });
    try {
      final loanId = await LoanApiService.applyLoan(
        amount: double.parse(_amountController.text),
        termMonths: int.parse(_termController.text),
      );
      Navigator.of(context).pushNamed(
        '/loan_status',
        arguments: loanId,
      );
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    } finally {
      setState(() {
        _isSubmitting = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('대출 신청')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _amountController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: '대출 금액'),
                validator: (v) => v == null || v.isEmpty
                    ? '금액을 입력하세요'
                    : null,
              ),
              TextFormField(
                controller: _termController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: '상환 기간(개월)'),
                validator: (v) => v == null || v.isEmpty
                    ? '기간을 입력하세요'
                    : null,
              ),
              const SizedBox(height: 20),
              if (_error != null)
                Text(
                  _error!,
                  style: const TextStyle(color: Colors.red),
                ),
              const SizedBox(height: 20),
              CustomButton(
                label: _isSubmitting ? '신청 중...' : '대출 신청',
                onPressed: _isSubmitting ? null : _submit,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
