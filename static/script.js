const socket = io("https://your-vercel-deploy.vercel.app");
const local = document.getElementById("local");
const remote = document.getElementById("remote");

let pc = new RTCPeerConnection();
navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(stream => {
  local.srcObject = stream;
  stream.getTracks().forEach(track => pc.addTrack(track, stream));
});

pc.ontrack = e => remote.srcObject = e.streams[0];

pc.onicecandidate = e => {
  if (e.candidate) socket.emit('ice', e.candidate);
};

socket.on('offer', async offer => {
  await pc.setRemoteDescription(offer);
  const answer = await pc.createAnswer();
  await pc.setLocalDescription(answer);
  socket.emit('answer', answer);
});

socket.on('answer', answer => pc.setRemoteDescription(answer));
socket.on('ice', ice => pc.addIceCandidate(ice));

function startCall() {
  pc.createOffer().then(offer => {
    pc.setLocalDescription(offer);
    socket.emit('offer', offer);
  });
}
