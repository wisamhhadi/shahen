class DriverModel {
  final int id;
  final String name;
  final String? phone;
  final String? status;
  final String? carNumber;

  DriverModel({required this.id, required this.name, this.phone, this.status, this.carNumber});

  factory DriverModel.fromJson(Map<String, dynamic> json) => DriverModel(
        id: int.tryParse("${json['id']}") ?? 0,
        name: "${json['name'] ?? 'سائق'}",
        phone: json['phone']?.toString(),
        status: json['status']?.toString(),
        carNumber: json['car_number']?.toString(),
      );
}
