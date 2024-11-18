from PySide6 import QtCore, QtGui, QtWidgets


def create_drop_shadow_image(
    path: str,
    output_path: str,
    shadow_radius: int = 32,
    shadow_offset: QtCore.QPoint = QtCore.QPoint(0, 4),
) -> None:
    QtWidgets.QApplication()

    pixmap = QtGui.QPixmap(path)

    # Graphics View
    view = QtWidgets.QGraphicsView()
    view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    # Graphics Scene
    rect = pixmap.rect()
    scene = QtWidgets.QGraphicsScene()
    scene_rect = QtCore.QRect(
        int((-shadow_radius + shadow_offset.x()) / 2),
        int((-shadow_radius + shadow_offset.y()) / 2),
        rect.width() + shadow_radius,
        rect.height() + shadow_radius,
    )
    scene.setSceneRect(scene_rect)
    view.setScene(scene)

    # Drop Shadow
    drop_shadow = QtWidgets.QGraphicsDropShadowEffect()
    drop_shadow.setOffset(shadow_offset)
    drop_shadow.setBlurRadius(shadow_radius)
    drop_shadow.setColor(QtGui.QColor(0, 0, 0, 128))

    # Image
    item = QtWidgets.QGraphicsPixmapItem(pixmap)
    item.setGraphicsEffect(drop_shadow)
    scene.addItem(item)

    # Save Scene to image
    image = QtGui.QImage(
        scene_rect.width(), scene_rect.height(), QtGui.QImage.Format.Format_ARGB32
    )
    image.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(image)
    scene.render(painter, target=QtCore.QRectF(image.rect()), source=scene_rect)
    painter.end()
    image.save(output_path)


if __name__ == '__main__':
    create_drop_shadow_image('./assets/icons.png', './assets/header.png')
