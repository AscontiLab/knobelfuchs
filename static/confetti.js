// Konfetti-Effekt bei richtiger Antwort
function launchConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const colors = ['#f97316', '#a855f7', '#ec4899', '#3b82f6', '#22c55e', '#eab308', '#ef4444', '#06b6d4'];
    const shapes = ['rect', 'circle', 'star', 'ribbon'];

    // Konfetti von mehreren Startpunkten
    const sources = [
        { x: canvas.width * 0.3, y: canvas.height * 0.5 },
        { x: canvas.width * 0.5, y: canvas.height * 0.4 },
        { x: canvas.width * 0.7, y: canvas.height * 0.5 },
    ];

    for (let s = 0; s < sources.length; s++) {
        for (let i = 0; i < 35; i++) {
            particles.push({
                x: sources[s].x + (Math.random() - 0.5) * 80,
                y: sources[s].y,
                vx: (Math.random() - 0.5) * 18,
                vy: Math.random() * -18 - 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                size: Math.random() * 8 + 3,
                shape: shapes[Math.floor(Math.random() * shapes.length)],
                rotation: Math.random() * 360,
                rotSpeed: (Math.random() - 0.5) * 12,
                gravity: 0.25 + Math.random() * 0.1,
                life: 1,
                decay: 0.006 + Math.random() * 0.004,
                wobble: Math.random() * Math.PI * 2,
                wobbleSpeed: 0.05 + Math.random() * 0.05,
            });
        }
    }

    function drawStar(ctx, x, y, size) {
        ctx.beginPath();
        for (let i = 0; i < 5; i++) {
            const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
            const method = i === 0 ? 'moveTo' : 'lineTo';
            ctx[method](x + size * Math.cos(angle), y + size * Math.sin(angle));
        }
        ctx.closePath();
        ctx.fill();
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let alive = false;

        for (const p of particles) {
            if (p.life <= 0) continue;
            alive = true;

            p.wobble += p.wobbleSpeed;
            p.x += p.vx + Math.sin(p.wobble) * 0.5;
            p.y += p.vy;
            p.vy += p.gravity;
            p.vx *= 0.99;
            p.rotation += p.rotSpeed;
            p.life -= p.decay;

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rotation * Math.PI / 180);
            ctx.globalAlpha = Math.min(p.life * 1.5, 1);
            ctx.fillStyle = p.color;

            switch (p.shape) {
                case 'rect':
                    ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size * 0.5);
                    break;
                case 'circle':
                    ctx.beginPath();
                    ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
                    ctx.fill();
                    break;
                case 'star':
                    drawStar(ctx, 0, 0, p.size / 2);
                    break;
                case 'ribbon':
                    ctx.fillRect(-p.size / 2, -p.size / 6, p.size, p.size / 3);
                    ctx.fillRect(-p.size / 6, -p.size / 2, p.size / 3, p.size);
                    break;
            }

            ctx.restore();
        }

        if (alive) {
            requestAnimationFrame(animate);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    animate();
}
