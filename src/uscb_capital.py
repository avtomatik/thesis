from thesis.src.lib.combine import combine_uscb_cap, combine_uscb_cap_deflator
from thesis.src.lib.plot import plot_uscb_cap, plot_uscb_cap_deflator
from thesis.src.lib.transform import transform_mean


def main() -> None:
    combine_uscb_cap().pipe(plot_uscb_cap)

    combine_uscb_cap_deflator().pipe(
        transform_mean, name="uscb_fused"
    ).pipe(plot_uscb_cap_deflator)


if __name__ == '__main__':
    main()
