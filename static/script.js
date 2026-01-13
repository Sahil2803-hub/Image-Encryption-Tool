function previewImage() {
  const input = document.getElementById('imageInput');
  const preview = document.getElementById('livePreview');

  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}
