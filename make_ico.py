import tempfile, os, sys

def make_lofi_ico(output_path="LofiGurl.ico"):
    from PIL import Image, ImageDraw

    def draw_girl(size):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        S = size / 64.0

        def s(x): return int(x * S)

        sk   = (232, 196, 154, 255)
        hair = (26,  8,   8,   255)
        ac   = (201, 169, 110, 255)
        hood = (30,  30,  46,  255)
        hood2= (22,  22,  42,  255)
        book = (201, 160, 80,  255)
        bg_c = (14,  14,  18,  255)
        dark = (14,  14,  18,  230)

        lw = max(1, s(1))

        # background circle
        d.ellipse([s(1), s(1), s(63), s(63)], fill=dark)

        # glow
        for r in range(s(26), 0, -2):
            a = int(35 * (1 - r / s(26)))
            d.ellipse([s(32)-r, s(32)-r, s(32)+r, s(32)+r], fill=(*ac[:3], a))

        # hoodie body
        d.rectangle([s(8), s(42), s(56), s(64)], fill=hood)
        d.rectangle([s(12), s(42), s(52), s(52)], fill=hood2)

        # neck
        d.rectangle([s(25), s(36), s(39), s(44)], fill=sk)

        # hair back
        d.ellipse([s(8), s(4), s(56), s(48)], fill=hair)

        # face
        d.ellipse([s(13), s(10), s(51), s(42)], fill=sk)

        # hair bang
        d.polygon([
            s(13),s(12), s(7),s(26), s(14),s(21),
            s(12),s(30), s(22),s(18), s(32),s(12)
        ], fill=hair)

        # glasses
        d.rectangle([s(14),s(20), s(27),s(29)], fill=ac, width=max(1,s(1)))
        d.rectangle([s(33),s(20), s(46),s(29)], fill=ac, width=max(1,s(1)))
        d.line([s(27),s(24), s(33),s(24)], fill=ac, width=max(1,s(1)))

        # eyes closed
        d.line([s(17),s(24), s(25),s(24)], fill=hair, width=max(1,s(1)))
        d.line([s(35),s(24), s(43),s(24)], fill=hair, width=max(1,s(1)))

        # smile
        d.arc([s(24),s(29), s(40),s(38)], start=200, end=340, fill=hair, width=max(1,s(1)))

        # headphones
        d.arc([s(6), s(5), s(20),s(30)], start=90,  end=270, fill=ac, width=max(2,s(2)))
        d.arc([s(44),s(5), s(58),s(30)], start=270, end=90,  fill=ac, width=max(2,s(2)))
        d.ellipse([s(3), s(13), s(12),s(24)], fill=ac)
        d.ellipse([s(52),s(13), s(61),s(24)], fill=ac)

        # book
        d.rectangle([s(7), s(49), s(57),s(62)], fill=book)
        d.line([s(32),s(49), s(32),s(62)], fill=bg_c, width=max(1,s(1)))
        d.line([s(10),s(54), s(30),s(54)], fill=bg_c, width=max(1,s(1)))
        d.line([s(10),s(58), s(30),s(58)], fill=bg_c, width=max(1,s(1)))
        d.line([s(34),s(54), s(54),s(54)], fill=bg_c, width=max(1,s(1)))

        return img

    sizes = [16, 32, 48, 64, 128, 256]
    images = [draw_girl(sz) for sz in sizes]

    images[0].save(
        output_path,
        format="ICO",
        sizes=[(sz, sz) for sz in sizes],
        append_images=images[1:]
    )
    print(f"Saved: {output_path}")
    return output_path

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "LofiGurl.ico"
    make_lofi_ico(out)
