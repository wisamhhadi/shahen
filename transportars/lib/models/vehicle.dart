class VehicleModel {
  final int id;
  final String name;
  final String? captainName;

  VehicleModel({required this.id, required this.name, this.captainName});

  factory VehicleModel.fromJson(Map<String, dynamic> json) => VehicleModel(
        id: int.tryParse("${json['id']}") ?? 0,
        name: "${json['car_number'] ?? json['name'] ?? 'مركبة'}",
        captainName: json['captain_name']?.toString(),
      );
}
