from Crypto.Util.number import long_to_bytes
from sympy import symbols, Poly, ZZ
from mpmath import mp, mpmathify
import numpy as np

# Set precision for mpmath
mp.dps = 200  # Increase this if precision issues persist

# Given data
n = 75611426846733548074395480486780420981996787746017992648766135297637412285786150518117412694353982730260339956103884006288811320733838224383508053272022147576879837387832237758766368883785181788819830865502742223519174450711328116138334507355907760483294595081173498453913346400135595506222134398989893494557
c = 24212544624137544627332056856124783218030228372400575745228195070749322642454653243200427755138872322964104254459633443311831377773274893652079118515291791542588544740764343640874607587628716007542872080742346529911701255688660521461743298540534157126929059855272833923180385515893193983225857155189935911538
e = 7

# Truncated plaintext
truncated_message = b"ketika bangga menjadi kontingen gemastik UI dan mendapatkan juara umum, tapi anda divisi 2, my honest impression: "
m_truncated = int.from_bytes(truncated_message, 'big')

# Polynomial construction
x = symbols('x', integer=True)
f = (m_truncated + x)**e - c
f = Poly(f, x, domain=ZZ)

# Lattice parameters
beta = 1 / e
X = int(n ** beta)  # Approximate bound for x
degree = f.degree()

# Create basis for lattice
def create_lattice(f, n, X):
    """Create a lattice basis matrix for LLL."""
    coeffs = f.all_coeffs()[::-1]  # Coefficients in ascending powers of x
    lattice_dim = len(coeffs)
    basis = np.zeros((lattice_dim, lattice_dim), dtype=object)

    for i in range(lattice_dim):
        for j in range(i + 1):
            basis[i, j] = coeffs[i - j] * (X**j) if i - j >= 0 else 0
        basis[i, i] = n if i != lattice_dim - 1 else 1

    return basis

# Apply LLL algorithm to reduce the lattice basis
def lll_reduction(basis):
    """Perform LLL reduction on the given lattice basis."""
    # Convert basis to mpmath format
    basis = np.array([[mpmathify(value) for value in row] for row in basis])
    m, n = basis.shape
    for i in range(m):
        for j in range(i):
            mu = basis[i, j] / basis[j, j]
            basis[i] -= mu * basis[j]

        norm_value = mp.sqrt(sum(val**2 for val in basis[i]))
        if i > 0 and norm_value < mp.sqrt(sum(val**2 for val in basis[i - 1])):
            basis[[i, i - 1]] = basis[[i - 1, i]]
    return basis

# Search for small roots
def find_small_root(f, n, X):
    """Find small roots of f modulo n using lattice reduction."""
    lattice = create_lattice(f, n, X)
    reduced_lattice = lll_reduction(lattice)

    for row in reduced_lattice:
        candidate_poly = Poly([int(mp.nint(val)) for val in row[:degree + 1]], x, domain=ZZ)
        for root in candidate_poly.real_roots():
            if root.is_integer and 0 <= root < X:
                return int(root)

    return None

# Recover the full message
small_root = find_small_root(f, n, X)
if small_root is not None:
    recovered_message = m_truncated + small_root
    print("Recovered Message:", long_to_bytes(recovered_message).decode())
else:
    print("No valid root found.")

