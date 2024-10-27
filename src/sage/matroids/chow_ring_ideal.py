r"""
Chow ring ideals of matroids

AUTHORS:

- Shriya M
"""

from sage.rings.polynomial.multi_polynomial_ideal import MPolynomialIdeal
from sage.matroids.utilities import cmp_elements_key
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.polynomial.multi_polynomial_sequence import PolynomialSequence
from sage.combinat.posets.posets import Poset

class ChowRingIdeal(MPolynomialIdeal):
    def matroid(self):
        r"""
        Return the matroid of the given Chow ring ideal.

        EXAMPLES::

            sage: ch = matroids.Uniform(3,6).chow_ring(QQ, False)
            sage: ch.defining_ideal().matroid()
            U(3, 6): Matroid of rank 3 on 6 elements with circuit-closures
            {3: {{0, 1, 2, 3, 4, 5}}}
        """
        M = self._matroid
        return M

    def flats_generator(self):
        r"""
        Return the variables of every corresponding flat/groundset element
        of the matroid.

        EXAMPLES::

            sage: ch = matroids.catalog.Fano().chow_ring(QQ, False)
            sage: ch.defining_ideal().flats_generator()
            {frozenset({'a'}): Aa, frozenset({'b'}): Ab, frozenset({'c'}): Ac,
             frozenset({'d'}): Ad, frozenset({'e'}): Ae, frozenset({'f'}): Af,
             frozenset({'g'}): Ag, frozenset({'a', 'b', 'f'}): Aabf,
             frozenset({'a', 'c', 'e'}): Aace,
             frozenset({'a', 'd', 'g'}): Aadg,
             frozenset({'b', 'c', 'd'}): Abcd,
             frozenset({'b', 'e', 'g'}): Abeg,
             frozenset({'c', 'f', 'g'}): Acfg,
             frozenset({'d', 'e', 'f'}): Adef,
             frozenset({'a', 'b', 'c', 'd', 'e', 'f', 'g'}): Aabcdefg}
        """
        return dict(self._flats_generator)


class ChowRingIdeal_nonaug(ChowRingIdeal):
    r"""
    The Chow ring ideal of a matroid `M`.

    The *Chow ring ideal* for a matroid `M` is defined as the ideal
    `(I_M + J_M)` of the polynomial ring

    .. MATH::

        R[x_{F_1}, \ldots, x_{F_k}],

    where

    - `F_1, \ldots, F_k` are the non-empty flats of `M`,
    - `I_M` is the Stanley-Reisner ideal, i.e., it is generated
      by products `x_{F_1}, \ldots, x_{F_t}` for subsets `\{F_1, \ldots, F_t\}`
      of flats that are not chains, and
    - `J_M` is the ideal generated by all linear forms

      .. MATH::

          \sum_{a \in F} x_F

      for all atoms `a` in the lattice of flats.

    INPUT:

    - ``M`` -- matroid
    - ``R`` -- commutative ring

    REFERENCES:

    - [ANR2023]_

    EXAMPLES:

    Chow ring ideal of uniform matroid of rank 3 on 6 elements::

        sage: ch = matroids.Uniform(3,6).chow_ring(QQ, False)
        sage: ch.defining_ideal()
        Chow ring ideal of U(3, 6): Matroid of rank 3 on 6 elements with
        circuit-closures {3: {{0, 1, 2, 3, 4, 5}}} - non augmented
        sage: ch = matroids.catalog.Fano().chow_ring(QQ, False)
        sage: ch.defining_ideal()
        Chow ring ideal of Fano: Binary matroid of rank 3 on 7 elements,
        type (3, 0) - non augmented
    """
    def __init__(self, M, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: I = matroids.catalog.Fano().chow_ring(QQ, False).defining_ideal()
            sage: TestSuite(I).run(skip="_test_category")
        """
        self._matroid = M
        flats = [X for i in range(1, self._matroid.rank() + 1)
                 for X in self._matroid.flats(i)]
        names = ['A{}'.format(''.join(str(x) for x in sorted(F, key=cmp_elements_key))) for F in flats]
        try:
            poly_ring = PolynomialRing(R, names) #self.ring
        except ValueError: # variables are not proper names
            poly_ring = PolynomialRing(R, 'A', len(flats))
        gens = poly_ring.gens()
        self._flats_generator = dict(zip(flats, gens))
        MPolynomialIdeal.__init__(self, poly_ring, self._gens_constructor(poly_ring))

    def _gens_constructor(self, poly_ring):
        r"""
        Return the generators of ``self``.

        EXAMPLES::

            sage: ch = matroids.catalog.NonFano().chow_ring(QQ, False)
            sage: ch.defining_ideal()._gens_constructor(ch.defining_ideal().ring())
            [Aa*Ab, Aa*Ac, Aa*Ae, Aa*Ad, Aa*Ade, Aa*Abcd, Aa*Af, Aa*Adf,
             Aa*Aef, Aa*Ag, Aa*Abeg, Aa*Acfg, Ab*Ac, Ab*Ae, Ab*Aace, Ab*Ad,
             Ab*Ade, Ab*Af, Ab*Adf, Ab*Aef, Ab*Ag, Ab*Aadg, Ab*Acfg, Ac*Ae,
             Ac*Ad, Ac*Ade, Ac*Af, Ac*Aabf, Ac*Adf, Ac*Aef, Ac*Ag, Ac*Aadg,
             Ac*Abeg, Ad*Ae, Ae*Abcd, Ae*Af, Ae*Aabf, Ae*Adf, Ae*Ag, Ae*Aadg,
             Ae*Acfg, Ad*Aace, Aace*Ade, Aace*Abcd, Af*Aace, Aabf*Aace,
             Aace*Adf, Aace*Aef, Ag*Aace, Aace*Aadg, Aace*Abeg, Aace*Acfg,
             Ad*Af, Ad*Aabf, Ad*Aef, Ad*Ag, Ad*Abeg, Ad*Acfg, Abcd*Ade, Af*Ade,
             Aabf*Ade, Ade*Adf, Ade*Aef, Ag*Ade, Aadg*Ade, Abeg*Ade, Acfg*Ade,
             Af*Abcd, Aabf*Abcd, Abcd*Adf, Abcd*Aef, Ag*Abcd, Aadg*Abcd,
             Abcd*Abeg, Abcd*Acfg, Af*Ag, Af*Aadg, Af*Abeg, Aabf*Adf, Aabf*Aef,
             Ag*Aabf, Aabf*Aadg, Aabf*Abeg, Aabf*Acfg, Adf*Aef, Ag*Adf,
             Aadg*Adf, Abeg*Adf, Acfg*Adf, Ag*Aef, Aadg*Aef, Abeg*Aef,
             Acfg*Aef, Aadg*Abeg, Aadg*Acfg, Abeg*Acfg,
             Aa + Aabf + Aace + Aadg + Aabcdefg,
             Ab + Aabf + Abcd + Abeg + Aabcdefg,
             Ac + Aace + Abcd + Acfg + Aabcdefg,
             Ad + Aadg + Abcd + Ade + Adf + Aabcdefg,
             Ae + Aace + Abeg + Ade + Aef + Aabcdefg,
             Af + Aabf + Acfg + Adf + Aef + Aabcdefg,
             Ag + Aadg + Abeg + Acfg + Aabcdefg]
        """
        flats = list(self._flats_generator)
        reln = lambda x,y: x <= y
        lattice_flats = Poset((flats, reln))
        I = []
        subsets = lattice_flats.antichains().elements_of_depth_iterator(2)
        for subset in subsets:
            term = poly_ring.one()
            for el in subset:
                term *= self._flats_generator[el]
            I.append(term) #Stanley-Reisner Ideal
        atoms = self._matroid.lattice_of_flats().atoms()
        atoms_gen = {a:poly_ring.zero() for a in atoms}
        for F in flats:
            for a in atoms:
                if a.issubset(F):
                    atoms_gen[a] += self._flats_generator[F]
        J = list(atoms_gen.values()) #Linear Generators
        return I + J

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: ch = matroids.catalog.Fano().chow_ring(QQ, False)
            sage: ch.defining_ideal()
            Chow ring ideal of Fano: Binary matroid of rank 3 on 7 elements,
            type (3, 0) - non augmented
        """
        return "Chow ring ideal of {} - non augmented".format(self._matroid)

    def _latex_(self):
        r"""
        Return a LaTeX representation of ``self``.

        EXAMPLES::

            sage: M1 = Matroid(groundset='abcd', bases=['ab','ad', 'bc'])
            sage: ch = M1.chow_ring(QQ, False)
            sage: ch.defining_ideal()._latex_()
            I_{M} + J_{M} of matroid \text{\texttt{Matroid{ }of{ }rank{ }2{ }on{ }4{ }elements{ }with{ }3{ }bases}}
        """
        from sage.misc.latex import latex
        return 'I_{M} + J_{M} of matroid ' + (latex(self._matroid))

    def groebner_basis(self, algorithm='', *args, **kwargs):
        r"""
        Return a Groebner basis of ``self``.

        EXAMPLES::

            sage: ch = Matroid(groundset='abc', bases=['ab', 'ac']).chow_ring(QQ, False)
            sage: ch.defining_ideal().groebner_basis()
            [Aa*Abc, Aa, Abc, Aa*Aabc, Abc*Aabc, Aabc]
            sage: ch.defining_ideal().groebner_basis().is_groebner()
            True

        Another example would be the Groebner basis of the Chow ring ideal of
        the matroid of the length 3 cycle graph::

            sage: ch = Matroid(graphs.CycleGraph(3)).chow_ring(QQ, False)
            sage: ch.defining_ideal().groebner_basis()
            [A0*A1, A0*A2, A1*A2, A0, A1, A2, A0*A3, A1*A3, A2*A3, A3]
            sage: ch.defining_ideal().groebner_basis().is_groebner()
            True
        """
        if algorithm == '':
            algorithm = 'constructed'
        if algorithm != 'constructed':
            return super().groebner_basis(algorithm=algorithm, *args, **kwargs)
        flats = sorted(list(self._flats_generator), key=len)
        ranks = {F: self._matroid.rank(F) for F in flats}
        gb = list()
        R = self.ring()
        reln = lambda x,y: x <= y
        flats_gen = self._flats_generator
        lattice_flats = Poset((flats, reln))
        antichains = lattice_flats.antichains().elements_of_depth_iterator(2)
        for subset in antichains: #Taking antichains of size 2
            term = R.one()
            for x in subset:
                term *= flats_gen[x]
            gb.append(term)
        for F in flats: #Reduced groebner basis by computing the sum first and then the product
            term = R.zero()
            for G in lattice_flats.order_filter([F]):
                term += flats_gen[G]
            for G in lattice_flats.order_ideal([F]):
                gb.append(flats_gen[G]*(term)**(ranks[F] - ranks[G]))
        g_basis = PolynomialSequence(R, [gb])
        return g_basis

class AugmentedChowRingIdeal_fy(ChowRingIdeal):
    r"""
    The augmented Chow ring ideal of matroid `M` over ring `R` in
    the Feitchner-Yuzvinsky presentation.

    The augmented Chow ring ideal for a matroid `M` is defined as the ideal
    `(I_M + J_M)` of the following polynomial ring

    .. MATH::

        R[y_{e_1}, \ldots, y_{e_n}, x_{F_1}, \ldots, x_{F_k}],

    where

    - `F_1, \ldots, F_k` are the proper flats of `M`,
    - `e_1, \ldots, e_n` are `n` elements of groundset of `M`,
    - `J_M` is the ideal generated by all quadratic forms `x_{F_i} x_{F_j}`,
      where `F_i` and `F_j` are incomparable elements in the lattice of
      flats and `y_{i} x_F` for every `i \in E` and `i \notin F`, and
    - `I_M` is the ideal generated by all linear forms

      .. MATH::

          y_i - \sum_{i \notin F} x_F

      for all `i \in E`.

    The augmented Chow ring ideal in the Feitchner-Yuzvinsky presentation
    for a simple matroid `M` is defined as the ideal `I_{FY}(M)` of the
    following polynomial ring

    .. MATH::

        R[y_{e_1}, \ldots, y_{e_n}, y_{F_1 \cup e}, \ldots, y_{F_k \cup e}],

    where

    - `F_1, \ldots, F_k` are the flats of `M`,
    - `e_1, \ldots, e_n` are `n` elements of groundset of `M`,
    - `I_{FY}(M)` is the ideal generated by all quadratic forms
      `y_{F_i \cup e} y_{F_j \cup e}`, where `F_i` and `F_j`
      are incomparable elements in the lattice of flats, `y_{i} y_{F \cup e}`
      for every `i \in E` and `i \notin F`, linear forms

      .. MATH::

          y_i + \sum_{i \in F} y_{F \cup e}

      for all `i \in E` and

      .. MATH::

          \sum_{F} y_{F \cup e}.

    Setting `x_F = y_{F \cup e}` and using the last linear
    form to eliminate `x_E` recovers the usual presentation of
    augmented Chow ring of `M`.

    REFERENCES:

    - [MM2022]_

    INPUT:

    - ``M`` -- matroid
    - ``R`` -- commutative ring

    EXAMPLES:

    Augmented Chow ring ideal of Wheel matroid of rank 3::

        sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'fy')
        sage: ch.defining_ideal()
        Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on 6
        elements with 16 bases of Feitchner-Yuzvinsky presentation
    """
    def __init__(self, M, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: I = matroids.Wheel(3).chow_ring(QQ, True, 'fy').defining_ideal()
            sage: TestSuite(I).run(skip="_test_category")
        """
        self._matroid = M
        self._flats = [X for i in range(self._matroid.rank() + 1)
                for X in self._matroid.flats(i)]
        E = list(self._matroid.groundset())
        self._flats_generator = dict()
        try:
            names_groundset = ['A{}'.format(''.join(str(x))) for x in E]
            names_flats = ['B{}'.format(''.join(str(x) for x in sorted(F, key=cmp_elements_key))) for F in self._flats]
            poly_ring = PolynomialRing(R, names_groundset + names_flats) #self.ring()
        except ValueError: #variables are not proper names
            poly_ring = PolynomialRing(R, 'A', len(E) + len(self._flats))
        for i,x in enumerate(E):
            self._flats_generator[x] = poly_ring.gens()[i]
        for i,F in enumerate(self._flats):
            self._flats_generator[F] = poly_ring.gens()[len(E) + i]
        MPolynomialIdeal.__init__(self, poly_ring, self._gens_constructor(poly_ring))

    def _gens_constructor(self, poly_ring):
        r"""
        Return the generators of ``self``.

        EXAMPLES::

            sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal()._gens_constructor(ch.defining_ideal().ring())
            [B0*B1, B0*B2, B0*B3, B0*B4, B0*B5, B0*B124, B0*B15, B0*B23,
             B0*B345, B0*B1, B1*B2, B1*B3, B1*B4, B1*B5, B1*B025, B1*B04,
             B1*B23, B1*B345, B0*B2, B1*B2, B2*B3, B2*B4, B2*B5, B2*B013,
             B2*B04, B2*B15, B2*B345, B0*B3, B1*B3, B2*B3, B3*B4, B3*B5,
             B3*B025, B3*B04, B3*B124, B3*B15, B0*B4, B1*B4, B2*B4, B3*B4,
             B4*B5, B4*B013, B4*B025, B4*B15, B4*B23, B0*B5, B1*B5, B2*B5,
             B3*B5, B4*B5, B5*B013, B5*B04, B5*B124, B5*B23, B2*B013, B4*B013,
             B5*B013, B013*B025, B013*B04, B013*B124, B013*B15, B013*B23,
             B013*B345, B1*B025, B3*B025, B4*B025, B013*B025, B025*B04,
             B025*B124, B025*B15, B025*B23, B025*B345, B1*B04, B2*B04, B3*B04,
             B5*B04, B013*B04, B025*B04, B04*B124, B04*B15, B04*B23, B04*B345,
             B0*B124, B3*B124, B5*B124, B013*B124, B025*B124, B04*B124,
             B124*B15, B124*B23, B124*B345, B0*B15, B2*B15, B3*B15, B4*B15,
             B013*B15, B025*B15, B04*B15, B124*B15, B15*B23, B15*B345, B0*B23,
             B1*B23, B4*B23, B5*B23, B013*B23, B025*B23, B04*B23, B124*B23,
             B15*B23, B23*B345, B0*B345, B1*B345, B2*B345, B013*B345,
             B025*B345, B04*B345, B124*B345, B15*B345, B23*B345, A0*B, A0*B1,
             A0*B2, A0*B3, A0*B4, A0*B5, A0*B124, A0*B15, A0*B23, A0*B345,
             A1*B, A1*B0, A1*B2, A1*B3, A1*B4, A1*B5, A1*B025, A1*B04, A1*B23,
             A1*B345, A2*B, A2*B0, A2*B1, A2*B3, A2*B4, A2*B5, A2*B013, A2*B04,
             A2*B15, A2*B345, A3*B, A3*B0, A3*B1, A3*B2, A3*B4, A3*B5, A3*B025,
             A3*B04, A3*B124, A3*B15, A4*B, A4*B0, A4*B1, A4*B2, A4*B3, A4*B5,
             A4*B013, A4*B025, A4*B15, A4*B23, A5*B, A5*B0, A5*B1, A5*B2,
             A5*B3, A5*B4, A5*B013, A5*B04, A5*B124, A5*B23,
             B + B0 + B1 + B2 + B3 + B4 + B5 + B013 + B025 + B04 + B124 + B15 + B23 + B345 + B012345,
             A0 + B0 + B013 + B025 + B04 + B012345,
             A1 + B1 + B013 + B124 + B15 + B012345,
             A2 + B2 + B025 + B124 + B23 + B012345,
             A3 + B3 + B013 + B23 + B345 + B012345,
             A4 + B4 + B04 + B124 + B345 + B012345,
             A5 + B5 + B025 + B15 + B345 + B012345]
        """
        E = list(self._matroid.groundset())
        flats_containing = {x: [] for x in E}
        for F in self._flats:
            for x in F:
                flats_containing[x].append(F)

        Q = list()
        L = list()
        term = poly_ring.zero()
        for F in self._flats:
            term += self._flats_generator[F]
            for G in self._flats:
                    if not (F <= G or G < F):
                        Q.append(self._flats_generator[F] * self._flats_generator[G]) #Quadratic Generators
        L.append(term)

        for x in E:
            term = poly_ring.zero()
            for F in self._flats:
                if F not in flats_containing[x]:
                    Q.append(self._flats_generator[x] * self._flats_generator[F])
                else:
                    term += self._flats_generator[F]
            L.append(self._flats_generator[x] + term) #Linear Generators
        return Q + L

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal()
            Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on
            6 elements with 16 bases of Feitchner-Yuzvinsky presentation
        """
        return "Augmented Chow ring ideal of {} of Feitchner-Yuzvinsky presentation".format(self._matroid)

    def _latex_(self):
        r"""
        Return a LaTeX representation of ``self``.

        EXAMPLES::

            sage: M1 = Matroid(graphs.CycleGraph(3))
            sage: ch = M1.chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal()._latex_()
            I_{FY} of matroid \text{\texttt{Graphic{ }matroid{ }of{ }rank{ }2{ }on{ }3{ }elements}}
        """
        from sage.misc.latex import latex
        return 'I_{FY} of matroid ' + (latex(self._matroid))

    def groebner_basis(self, algorithm='', *args, **kwargs):
        r"""
        Return the Groebner basis of ``self``.

        EXAMPLES::

            sage: ch = matroids.Uniform(2,5).chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal().groebner_basis(algorithm='')
            Polynomial Sequence with 565 Polynomials in 12 Variables
            sage: ch.defining_ideal().groebner_basis(algorithm='').is_groebner()
            True
        """
        if algorithm == '':
            algorithm = 'constructed'
        if algorithm != 'constructed':
            return super().groebner_basis(algorithm=algorithm, *args, **kwargs)
        gb = [] #Reduced groebner basis with two eliminated cases
        E = list(self._matroid.groundset())
        poly_ring = self.ring()
        for F in self._flats:
            for G in self._flats:
                if not (F <= G or G <= F): #Non-nested flats
                        gb.append(self._flats_generator[F]*self._flats_generator[G])

                for i in E:
                    term = poly_ring.zero()
                    term1 = poly_ring.zero()
                    for H in self._flats:
                        if i in H:
                            term += self._flats_generator[H]
                        if H >= G:
                            term1 += self._flats_generator[H]
                    if term != poly_ring.zero():
                        gb.append(self._flats_generator[i] + term) #5.7
                    if term1 != poly_ring.zero():
                        gb.append(term1**(self._matroid.rank(G) + 1)) #5.6

                    if G > F: #nested flats
                        if term1 != poly_ring.zero():
                            gb.append(self._flats_generator[F]*term1**(self._matroid.rank(G)-self._matroid.rank(F)))

        g_basis = PolynomialSequence(poly_ring, [gb])
        return g_basis

class AugmentedChowRingIdeal_atom_free(ChowRingIdeal):
    r"""
    The augmented Chow ring ideal for a matroid `M` over ring `R` in the
    atom-free presentation.

    The augmented Chow ring ideal in the atom-free presentation for a matroid
    `M` is defined as the ideal `I_{af}(M)` of the polynomial ring:

    .. MATH::

        R[x_{F_1}, \ldots, x_{F_k}],

    where

    - `F_1, \ldots, F_k` are the non-empty flats of `M`,
    - `I_{af}(M)` is the ideal generated by all quadratic forms `x_{F_i} x_{F_j}`
      where `F_i` and `F_j` are incomparable elements in the lattice of flats,

      .. MATH::

        x_F \sum_{i \in F'} x_{F'}

      for all `i \in E` and `i \notin F`, and

      .. MATH::

        \sum_{i \in F'} (x_{F'})^2

      for all `i \in E`.

    REFERENCES:

    - [MM2022]_

    INPUT:

    - ``M`` -- matroid
    - ``R`` -- commutative ring

    EXAMPLES:

    Augmented Chow ring ideal of Wheel matroid of rank 3::

        sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'atom-free')
        sage: ch.defining_ideal()
        Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on 6
        elements with 16 bases in the atom-free presentation
    """
    def __init__(self, M, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: I = matroids.Wheel(3).chow_ring(QQ, True, 'atom-free').defining_ideal()
            sage: TestSuite(I).run(skip="_test_category")
        """
        self._matroid = M
        self._flats = [X for i in range(1, self._matroid.rank() + 1)
                 for X in self._matroid.flats(i)]
        names = ['A{}'.format(''.join(str(x) for x in sorted(F, key=cmp_elements_key))) for F in self._flats]
        try:
            poly_ring = PolynomialRing(R, names) #self.ring
        except ValueError: # variables are not proper names
            poly_ring = PolynomialRing(R, 'A', len(self._flats))
        gens = poly_ring.gens()
        self._flats_generator = dict(zip(self._flats, gens))
        MPolynomialIdeal.__init__(self, poly_ring, self._gens_constructor(poly_ring))

    def _gens_constructor(self, poly_ring):
        r"""
        Return the generators of ``self``.

        EXAMPLES::

            sage: M1 = Matroid(graphs.CycleGraph(3))
            sage: ch = M1.chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal()._gens_constructor(ch.defining_ideal().ring())
            [A0*A1, A0*A2, A0^2 + 2*A0*A3 + A3^2, A1^2 + 2*A1*A3 + A3^2,
             A0*A1 + A0*A3, A2^2 + 2*A2*A3 + A3^2, A0*A2 + A0*A3,
             A0*A1, A1*A2, A0*A1 + A1*A3, A1*A2 + A1*A3, A0*A2, A1*A2,
             A0*A2 + A2*A3, A1*A2 + A2*A3]
        """
        E = list(self._matroid.groundset())
        Q = [] #Quadratic Generators
        flats_containing = {x: [] for x in E}
        for F in self._flats:
            for x in F:
                flats_containing[x].append(F)
        for F in self._flats:
            for G in self._flats:
                if not (G >= F or F > G): #generators for every pair of non-nested flats
                        Q.append(self._flats_generator[F]*self._flats_generator[G])
            for x in E: #generators for every set of flats containing element
                term = poly_ring.zero()
                for H in flats_containing[x]:
                    term += self._flats_generator[H]
                if term**2 not in Q:
                    Q.append(term**2)

                if F not in flats_containing[x]: #generators for every set of flats not containing element
                    Q.append(self._flats_generator[F]*term)
        return Q

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal()
            Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on
            6 elements with 16 bases in the atom-free presentation
        """
        return "Augmented Chow ring ideal of {} in the atom-free presentation".format(self._matroid)

    def _latex_(self):
        r"""
        Return the LaTeX output of the ring and generators of ``self``.

        EXAMPLES::

            sage: M1 = Matroid(graphs.CycleGraph(3))
            sage: ch = M1.chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal()._latex_()
            I_{af} of matroid \text{\texttt{Graphic{ }matroid{ }of{ }rank{ }2{ }on{ }3{ }elements}}
        """
        from sage.misc.latex import latex
        return 'I_{af} of matroid ' + latex(self._matroid)

    def groebner_basis(self, algorithm='', *args, **kwargs):
        """
        Return the Groebner basis of ``self``.

        EXAMPLES::

            sage: M1 = Matroid(graphs.CycleGraph(3))
            sage: ch = M1.chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal().groebner_basis(algorithm='')
            Polynomial Sequence with 22 Polynomials in 3 Variables
            sage: ch.defining_ideal().groebner_basis(algorithm='').is_groebner()
            True
        """
        if algorithm == '':
            algorithm = 'constructed'
        if algorithm != 'constructed':
            return super().groebner_basis(algorithm=algorithm, *args, **kwargs)
        gb = []
        poly_ring = self.ring()
        for F in self._flats:
            for G in self._flats:
                term = poly_ring.zero()
                for H in self._flats:
                    if H < F:
                        term += self._flats_generator[H]
                if not (F >= G or G > F): #Non nested flats
                    gb.append(self._flats_generator[F]*self._flats_generator[G])
                elif F < G: #Nested flats
                    if term != poly_ring.zero():
                        gb.append(self._flats_generator[F]*(term**(self._matroid.rank(G) - self._matroid.rank(F))))
                gb.append((term**self._matroid.rank(F)) + 1)

        g_basis = PolynomialSequence(poly_ring, [gb])
        return g_basis