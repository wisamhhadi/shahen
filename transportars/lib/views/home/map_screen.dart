import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../../models/transporter.dart';
import '../../services/links.dart';
import '../../services/network.dart';

class TransporterMapScreen extends StatefulWidget {
  final Transporter? transporter;

  const TransporterMapScreen({
    super.key,
    this.transporter,
  });

  @override
  State<TransporterMapScreen> createState() => _TransporterMapScreenState();
}

class _TransporterMapScreenState extends State<TransporterMapScreen> {
  final Network net = Network();

  GoogleMapController? mapController;
  bool loading = true;

  final Set<Marker> markers = {};
  LatLng initialPosition = const LatLng(30.5081, 47.7835); // Basra

  @override
  void initState() {
    super.initState();
    loadDriversOnMap();
  }

  double? toDouble(dynamic value) {
    if (value == null) return null;

    final text = value.toString().trim();
    if (text.isEmpty || text == 'null' || text == 'None') return null;

    return double.tryParse(text);
  }

  LatLng? pointFromJson(Map<String, dynamic> json) {
    final lat = toDouble(
      json['latitude2'] ??
          json['lat2'] ??
          json['latitude'] ??
          json['lat'] ??
          json['latitude_base'],
    );

    final lng = toDouble(
      json['longitude2'] ??
          json['lng2'] ??
          json['longitude'] ??
          json['lng'] ??
          json['longitude_base'],
    );

    if (lat == null || lng == null) return null;
    if (lat.abs() > 90 || lng.abs() > 180) return null;

    return LatLng(lat, lng);
  }

  Future<void> loadDriversOnMap() async {
    setState(() => loading = true);

    final newMarkers = <Marker>{};

    try {
      final drivers = await net.getList(Links.drivers);

      for (final item in drivers) {
        if (item is! Map) continue;

        final driver = Map<String, dynamic>.from(item);
        final point = pointFromJson(driver);

        if (point == null) continue;

        final id = int.tryParse('${driver['id'] ?? 0}') ?? newMarkers.length;
        final name = '${driver['name'] ?? 'سائق'}';
        final phone = '${driver['phone'] ?? ''}';

        if (newMarkers.isEmpty) {
          initialPosition = point;
        }

        newMarkers.add(
          Marker(
            markerId: MarkerId('driver_$id'),
            position: point,
            icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueAzure),
            infoWindow: InfoWindow(title: name, snippet: phone),
            onTap: () => showDriverInfo(driver),
          ),
        );
      }

      if (!mounted) return;

      setState(() {
        markers
          ..clear()
          ..addAll(newMarkers);
      });

      if (mapController != null && markers.isNotEmpty) {
        await moveCameraToMarkers();
      }
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('تعذر تحميل مواقع السائقين: $e')),
      );
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> moveCameraToMarkers() async {
    if (mapController == null || markers.isEmpty) return;

    if (markers.length == 1) {
      await mapController!.animateCamera(
        CameraUpdate.newLatLngZoom(markers.first.position, 15),
      );
      return;
    }

    double minLat = markers.first.position.latitude;
    double maxLat = markers.first.position.latitude;
    double minLng = markers.first.position.longitude;
    double maxLng = markers.first.position.longitude;

    for (final marker in markers) {
      final p = marker.position;

      if (p.latitude < minLat) minLat = p.latitude;
      if (p.latitude > maxLat) maxLat = p.latitude;
      if (p.longitude < minLng) minLng = p.longitude;
      if (p.longitude > maxLng) maxLng = p.longitude;
    }

    await mapController!.animateCamera(
      CameraUpdate.newLatLngBounds(
        LatLngBounds(
          southwest: LatLng(minLat, minLng),
          northeast: LatLng(maxLat, maxLng),
        ),
        80,
      ),
    );
  }

  void showDriverInfo(Map<String, dynamic> driver) {
    showModalBottomSheet(
      context: context,
      showDragHandle: true,
      builder: (_) {
        return Directionality(
          textDirection: TextDirection.rtl,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(18, 8, 18, 24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  '${driver['name'] ?? 'سائق'}',
                  style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text('الهاتف: ${driver['phone'] ?? '-'}'),
                Text('الحالة: ${driver['status'] ?? '-'}'),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(22),
      child: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: initialPosition,
              zoom: 12,
            ),
            markers: markers,
            zoomControlsEnabled: false,
            myLocationButtonEnabled: false,
            compassEnabled: true,
            onMapCreated: (controller) async {
              mapController = controller;

              if (markers.isNotEmpty) {
                await moveCameraToMarkers();
              }
            },
          ),
          Positioned(
            top: 12,
            right: 12,
            child: Material(
              color: Colors.white,
              elevation: 3,
              borderRadius: BorderRadius.circular(12),
              child: InkWell(
                onTap: loadDriversOnMap,
                borderRadius: BorderRadius.circular(12),
                child: const Padding(
                  padding: EdgeInsets.all(10),
                  child: Icon(Icons.refresh, color: Color(0xFF1E9B4B)),
                ),
              ),
            ),
          ),
          if (loading)
            const Positioned.fill(
              child: ColoredBox(
                color: Color(0x33FFFFFF),
                child: Center(child: CircularProgressIndicator()),
              ),
            ),
          if (!loading && markers.isEmpty)
            Positioned(
              left: 12,
              right: 12,
              bottom: 12,
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.95),
                  borderRadius: BorderRadius.circular(14),
                  boxShadow: const [
                    BoxShadow(
                      color: Color(0x22000000),
                      blurRadius: 8,
                      offset: Offset(0, 3),
                    ),
                  ],
                ),
                child: const Text(
                  'الخريطة تعمل، لكن لا توجد مواقع سائقين حالياً. أضف سائقاً مع خط العرض والطول أو حدّث موقع السائق من تطبيق السائقين.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF1E9B4B),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
